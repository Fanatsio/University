import os

import pickle

import time

import requests

from bs4 import BeautifulSoup

from collections import deque

import re

import numpy as np

import math

import nltk

from nltk.corpus import stopwords

from nltk import word_tokenize

from nltk.stem import WordNetLemmatizer

from nltk.corpus import wordnet

from flask import Flask, request, render_template_string, redirect



app = Flask(__name__)



GLOBAL_DOCS = {}

GLOBAL_INV = {}

GLOBAL_DL = {}

GLOBAL_PR = {}



IMPRESSIONS = {}

CLICKS = {}

DWELL = {}

BOUNCE_COUNT = {}

SESSION_START = {}

SESSION_URL = {}



def crawl_web(seed_urls, max_depth=2, max_pages=200):

    visited = set()

    docs_content = {}

    adj_list = {}

    queue = deque([(url, 0) for url in seed_urls])

    while queue and len(docs_content) < max_pages:

        current_url, depth = queue.popleft()

        if current_url in visited:

            continue

        visited.add(current_url)

        if depth > max_depth:

            continue

        try:

            resp = requests.get(current_url, timeout=5)

            if resp.status_code != 200:

                continue

            html = resp.text

        except:

            continue

        soup = BeautifulSoup(html, 'html.parser')

        for s in soup(['script','style']):

            s.decompose()

        text = re.sub(r'\s+',' ', soup.get_text(separator=' ')).strip()

        title_tag = soup.find('title')

        title = title_tag.get_text().strip() if title_tag else current_url

        docs_content[current_url] = {"title": title, "text": text}

        links_on_page = []

        for link_tag in soup.find_all('a', href=True):

            href = link_tag['href']

            full_link = requests.compat.urljoin(current_url, href)

            full_link = re.split(r'#|\?', full_link)[0]

            if full_link.startswith('http'):

                links_on_page.append(full_link)

                if full_link not in visited:

                    queue.append((full_link, depth+1))

        adj_list[current_url] = list(set(links_on_page))

    return docs_content, adj_list



def get_wordnet_pos(tag):

    if tag.startswith('J'):

        return wordnet.ADJ

    elif tag.startswith('V'):

        return wordnet.VERB

    elif tag.startswith('N'):

        return wordnet.NOUN

    elif tag.startswith('R'):

        return wordnet.ADV

    return wordnet.NOUN



def tokenize_lemma(text):

    text = text.lower()

    tokens = word_tokenize(text)

    russian_stop = set(stopwords.words('russian'))

    tokens = [re.sub(r'[^а-яёa-z]+','', w) for w in tokens]

    tokens = [w for w in tokens if w and w not in russian_stop]

    lemmatizer = WordNetLemmatizer()

    return [lemmatizer.lemmatize(w) for w in tokens]



def build_inverted_index(docs_content):

    inv_index = {}

    doc_lengths = {}

    for url, data in docs_content.items():

        toks = tokenize_lemma(data["text"])

        doc_lengths[url] = len(toks)

        for pos, token in enumerate(toks):

            if token not in inv_index:

                inv_index[token] = {}

            if url not in inv_index[token]:

                inv_index[token][url] = {"freq": 0, "positions": []}

            inv_index[token][url]["freq"] += 1

            inv_index[token][url]["positions"].append(pos)

    return inv_index, doc_lengths



def build_adjacency_matrix(adj_list):

    urls = list(adj_list.keys())

    url_to_id = {u: i for i,u in enumerate(urls)}

    n = len(urls)

    matrix = np.zeros((n,n), dtype=float)

    for u in urls:

        i = url_to_id[u]

        outlinks = adj_list[u]

        if not outlinks:

            matrix[i,:] = 1.0/n

        else:

            for v in outlinks:

                if v in url_to_id:

                    j = url_to_id[v]

                    matrix[i,j] = 1.0

    for i in range(n):

        row_sum = np.sum(matrix[i,:])

        if row_sum>0:

            matrix[i,:] /= row_sum

        else:

            matrix[i,:] = 1.0/n

    return matrix, urls, url_to_id



def pagerank(matrix, d=0.85, tol=1e-6, max_iter=100):

    n = matrix.shape[0]

    pr = np.ones(n)/n

    for _ in range(max_iter):

        new_pr = (1-d)/n + d*np.dot(matrix.T, pr)

        if np.linalg.norm(new_pr - pr,1)<tol:

            pr = new_pr

            break

        pr = new_pr

    return pr



def compute_idf(inverted_index, total_docs):

    idf_dict = {}

    for term, posting in inverted_index.items():

        df = len(posting)

        val = math.log((total_docs - df + 0.5)/(df + 0.5) + 1)

        idf_dict[term] = val

    return idf_dict



def bm25_score(query_tokens, url, inv_index, doc_lengths, idf_dict, avgdl, k1=1.2, b=0.75):

    score = 0.0

    dl = doc_lengths[url]

    for t in query_tokens:

        if t not in inv_index:

            continue

        if url not in inv_index[t]:

            continue

        freq = inv_index[t][url]["freq"]

        numerator = freq*(k1+1)

        denominator = freq + k1*(1 - b + b*(dl/avgdl))

        score += idf_dict.get(t,0)*(numerator/denominator)

    return score



def combined_score(url, bm25_val, pr_val):

    impressions = IMPRESSIONS.get(url, 0)

    clicks = CLICKS.get(url,0)

    if impressions == 0:

        real_ctr = 0

    else:

        real_ctr = clicks/impressions



    dwell = DWELL.get(url,0)

    bounce_cnt = BOUNCE_COUNT.get(url,0)

    return bm25_val + 0.5*pr_val + 2*real_ctr + 0.01*dwell - bounce_cnt



def combined_ranking(query_tokens, inv_index, doc_lengths, docs_content, pr_dict):

    candidates = set()

    for t in query_tokens:

        if t in inv_index:

            candidates |= set(inv_index[t].keys())

    if not candidates:

        return []

    total_docs = len(docs_content)

    idf_dict = compute_idf(inv_index, total_docs)

    avgdl = sum(doc_lengths.values())/total_docs if total_docs>0 else 1

    results = []

    for url in candidates:

        bm25_val = bm25_score(query_tokens, url, inv_index, doc_lengths, idf_dict, avgdl)

        pr_val = pr_dict.get(url, 0)

        final_val = combined_score(url, bm25_val, pr_val)

        results.append((url, final_val))

    results.sort(key=lambda x: x[1], reverse=True)

    return results



def get_session_id():

    s = request.cookies.get('session_id')

    if not s:

        s = str(int(time.time()*1000)) + str(np.random.randint(100000))

    return s



def save_data():

    data = {

        "docs": GLOBAL_DOCS,

        "inv": GLOBAL_INV,

        "dl": GLOBAL_DL,

        "pr": GLOBAL_PR,

        "imp": IMPRESSIONS,

        "clk": CLICKS,

        "dw": DWELL,

        "bc": BOUNCE_COUNT

    }

    with open("search_data.pkl","wb") as f:

        pickle.dump(data, f)



@app.route("/")

def index_page():

    html = """

    <h2>Поисковая система</h2>

    <form action="/search" method="get">

      <input type="text" name="q" placeholder="Запрос" size="40" />

      <input type="submit" value="Искать" />

    </form>

    """

    return html



@app.route("/search")

def search_page():

    query = request.args.get("q","").strip()

    if not query:

        return "Пустой запрос. <a href='/'>Назад</a>"

    page = int(request.args.get("page","1"))

    tokens = tokenize_lemma(query)

    results = combined_ranking(tokens, GLOBAL_INV, GLOBAL_DL, GLOBAL_DOCS, GLOBAL_PR)

    if not results:

        return f"Ничего не найдено для <b>{query}</b>. <a href='/'>Назад</a>"



    for (url, _) in results:

        IMPRESSIONS[url] = IMPRESSIONS.get(url,0)+1



    per_page = 20

    total_pages = (len(results)+per_page-1)//per_page

    start = (page-1)*per_page

    end = start+per_page

    subset = results[start:end]



    h = f"<h3>Результаты для: {query}</h3>"

    h += f"<p>Всего: {len(results)}. Страница {page}/{total_pages}</p>"

    h += "<ol>"

    for (url, score) in subset:

        title = GLOBAL_DOCS[url]["title"]

        h += f"<li><a href='/click?target={url}&q={query}' target='_blank'>{title}</a> (score={score:.3f})</li>"

    h += "</ol>"



    if page>1:

        h += f"<a href='/search?q={query}&page={page-1}'>Предыдущая</a> "

    if page<total_pages:

        h += f"<a href='/search?q={query}&page={page+1}'>Следующая</a> "



    h += "<br><a href='/'>Новый поиск</a>"

    return h



@app.route("/click")

def click_doc():

    target = request.args.get("target","")

    if not target:

        return "Ошибка: нет ссылки"

    CLICKS[target] = CLICKS.get(target,0)+1

    s_id = get_session_id()

    SESSION_START[s_id] = time.time()

    SESSION_URL[s_id] = target

    save_data()

    return redirect(target)



@app.route("/return_to_results")

def return_to_results():

    s_id = get_session_id()

    if s_id in SESSION_START:

        delta = time.time() - SESSION_START[s_id]

        doc_url = SESSION_URL[s_id]

        DWELL[doc_url] = DWELL.get(doc_url,0)+delta

        if delta<5:

            BOUNCE_COUNT[doc_url] = BOUNCE_COUNT.get(doc_url,0)+1

        del SESSION_START[s_id]

        del SESSION_URL[s_id]

    save_data()

    return "Вы вернулись на результаты. <a href='/'>Главная</a>"



def run_app():

    global GLOBAL_DOCS, GLOBAL_INV, GLOBAL_DL, GLOBAL_PR

    global IMPRESSIONS, CLICKS, DWELL, BOUNCE_COUNT



    if os.path.exists("search_data.pkl"):

        with open("search_data.pkl","rb") as f:

            data = pickle.load(f)

            GLOBAL_DOCS = data["docs"]

            GLOBAL_INV = data["inv"]

            GLOBAL_DL = data["dl"]

            GLOBAL_PR = data["pr"]

            IMPRESSIONS = data.get("imp",{})

            CLICKS = data.get("clk",{})

            DWELL = data.get("dw",{})

            BOUNCE_COUNT = data.get("bc",{})

    else:

        seed_urls = [

            "https://ru.wikipedia.org/wiki/Мастер_и_Маргарита",

            "https://ru.wikipedia.org/wiki/Кот"

        ]

        docs_content, adj_list = crawl_web(seed_urls,2,50)

        inv, dl = build_inverted_index(docs_content)

        mat, urls, _ = build_adjacency_matrix(adj_list)

        pr_vals = pagerank(mat)

        pr_dict = {}

        for i,u in enumerate(urls):

            pr_dict[u] = pr_vals[i]

        GLOBAL_DOCS = docs_content

        GLOBAL_INV = inv

        GLOBAL_DL = dl

        GLOBAL_PR = pr_dict

        IMPRESSIONS = {}

        CLICKS = {}

        DWELL = {}

        BOUNCE_COUNT = {}

        save_data()



    app.run(debug=True, port=5000)



if __name__ == "__main__":

    run_app()
