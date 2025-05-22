import os

import re

import pickle

import requests

import numpy as np

import pandas as pd

import nltk

from collections import deque

from bs4 import BeautifulSoup

from nltk.tokenize import word_tokenize

from nltk.stem.snowball import SnowballStemmer

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

from urllib.parse import urlparse, urlunparse, unquote



nltk.download("punkt")



stemmer = SnowballStemmer("russian")



MODEL_FILE = "ml_model.pkl"

DATASET_FILE = "dataset.csv"

K_TOP_BM25 = 5  



def preprocess_text(text):

    tokens = word_tokenize(text.lower())

    processed_tokens = [stemmer.stem(word) for word in tokens if word.isalnum()]

    return " ".join(processed_tokens)



def normalize_url(url):

    p = urlparse(url)

    return urlunparse((p.scheme.lower(), p.netloc.lower(), p.path, '', '', ''))



def crawl_web(seed_urls, max_depth=2, max_pages=50):

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

        except Exception:

            continue

        soup = BeautifulSoup(html, 'html.parser')

        for s in soup(['script', 'style']):

            s.decompose()

        text = re.sub(r'\s+', ' ', soup.get_text(separator=' ')).strip()

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

                    queue.append((full_link, depth + 1))

        adj_list[current_url] = list(set(links_on_page))

    return docs_content, adj_list



def load_data():

    if os.path.exists("search_data.pkl"):

        with open("search_data.pkl", "rb") as f:

            data = pickle.load(f)

        docs_content = data["docs"]

    else:

        seed_urls = ["https://ru.wikipedia.org/wiki/Поисковый_робот",

                     "https://habr.com/ru/articles/"]



        docs_content, adj_list = crawl_web(seed_urls, max_depth=2, max_pages=50)

        data = {"docs": docs_content, "adj": adj_list}

        with open("search_data.pkl", "wb") as f:

            pickle.dump(data, f)

    documents = {}

    for url, info in docs_content.items():

        norm_url = normalize_url(url)

        documents[norm_url] = info["text"]

    return documents



def compute_bm25_score(query, documents, k1=1.5, b=0.75):

    processed_query = preprocess_text(query)

    query_words = processed_query.split()

    

    doc_urls = list(documents.keys())

    doc_texts = list(documents.values())

    

    vectorizer = CountVectorizer()

    X = vectorizer.fit_transform(doc_texts)

    terms = vectorizer.get_feature_names_out()

    X_array = X.toarray()

    

    df = np.sum(X_array > 0, axis=0)

    idf = np.log((len(doc_texts) - df + 0.5) / (df + 0.5) + 1)

    

    doc_lengths = np.sum(X_array, axis=1)

    avg_doc_length = np.mean(doc_lengths)

    

    scores = []

    for i, doc_vec in enumerate(X_array):

        doc_length = doc_lengths[i]

        score = 0.0

        for word in query_words:

            if word in terms:

                idx = np.where(terms == word)[0][0]

                tf = doc_vec[idx]

                if tf > 0:

                    score += idf[idx] * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_length / avg_doc_length))))

        scores.append((doc_urls[i], score))

    

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores



def dcg(relevances):

    total = 0.0

    for i, rel in enumerate(relevances):

        total += (2**rel - 1) / np.log2(i + 2)

    return total



def ndcg(relevances):

    ideal = sorted(relevances, reverse=True)

    best = dcg(ideal)

    return dcg(relevances) / best if best > 0 else 0.0



def compute_metrics(ranked_relevances, K=5, total_relevant=None):

    top_k = ranked_relevances[:K]

    precision = sum(top_k) / K

    if total_relevant is None:

        total_relevant = sum(ranked_relevances)

    recall = sum(top_k) / total_relevant if total_relevant > 0 else 0

    ndcg_val = ndcg(top_k)

    return precision, recall, ndcg_val



def train_or_load_model():

    if os.path.exists(MODEL_FILE):

        print(f"Модель уже обучена. Загружаем {MODEL_FILE}...")

        with open(MODEL_FILE, "rb") as f:

            model = pickle.load(f)

        return model



    print("🚀 Обучаем ML-модель...")

    documents = load_data()

    queries = ["робот", "алгоритм", "page", "спорт", "система", "человек"]



    data_rows = []

    for query in queries:

        bm25_results = compute_bm25_score(query, documents)

        for rank, (doc_url, bm25_score) in enumerate(bm25_results):

            relevance = 1 if rank < K_TOP_BM25 else 0

            content = documents[doc_url]

            tokens = content.split()

            doc_length = len(tokens)

            processed_query_tokens = preprocess_text(query).split()

            position = float('inf')

            for token in processed_query_tokens:

                try:

                    pos = tokens.index(token)

                    if pos < position:

                        position = pos

                except ValueError:

                    continue

            if position == float('inf'):

                position = -1

            position_score = 1 / (position + 1) if position != -1 else 0

            data_rows.append([query, doc_url, doc_length, position_score, bm25_score, relevance])

    

    df = pd.DataFrame(data_rows, columns=["query", "doc_url", "doc_length", "position_score", "bm25_score", "relevance"])

    df.to_csv(DATASET_FILE, index=False, encoding="utf-8")

    

    X = df[["doc_length", "position_score", "bm25_score"]]

    y = df["relevance"]



    if len(y.unique()) < 2:

        print(" Ошибка: В выборке только один класс!")

        return None

    

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000)

    model.fit(X_train, y_train)

    

    accuracy = model.score(X_test, y_test)

    print(f" Точность модели на тестовых данных: {accuracy:.4f}")

    

    with open(MODEL_FILE, "wb") as f:

        pickle.dump(model, f)

    print(f" Модель обучена и сохранена в {MODEL_FILE}!")

    return model



def run_ranking():

    model = train_or_load_model()

    if model is None:

        return



    documents = load_data()

    queries = ["робот", "алгоритм", "page", "спорт", "система", "человек"]



    print("\n Сравнение ML vs BM25")

    for query in queries:

        print(f"\n Запрос: {query}")

        bm25_results = compute_bm25_score(query, documents)

        bm25_top_docs = set([doc for doc, score in bm25_results[:K_TOP_BM25]])

        

        rows = []

        processed_query_tokens = preprocess_text(query).split()

        for doc_url, content in documents.items():

            tokens = content.split()

            doc_length = len(tokens)

            position = float('inf')

            for token in processed_query_tokens:

                try:

                    pos = tokens.index(token)

                    if pos < position:

                        position = pos

                except ValueError:

                    continue

            if position == float('inf'):

                position = -1

            position_score = 1 / (position + 1) if position != -1 else 0

            bm25_score = next((score for url, score in bm25_results if url == doc_url), 0)

            rows.append([doc_url, doc_length, position_score, bm25_score])

        

        query_df = pd.DataFrame(rows, columns=["doc_url", "doc_length", "position_score", "bm25_score"])

        X_features = query_df[["doc_length", "position_score", "bm25_score"]]

        ml_probs = model.predict_proba(X_features)[:, 1]

        query_df["ml_score"] = ml_probs

        

        query_df_ml = query_df.sort_values("ml_score", ascending=False)

        

        print("\n ML топ-5:")

        for _, row in query_df_ml.head(K_TOP_BM25).iterrows():

            print(f"{unquote(row['doc_url'])} - Score: {row['ml_score']:.4f}")

        

        print("\n BM25 топ-5:")

        for doc, score in bm25_results[:K_TOP_BM25]:

            print(f"{unquote(doc)} - Score: {score:.4f}")

        

        ground_truth = [1 if doc in bm25_top_docs else 0 for doc in query_df_ml["doc_url"]]

        precision, recall, ndcg_val = compute_metrics(ground_truth, K=K_TOP_BM25, total_relevant=sum(ground_truth))

        print(f"\nМетрики для ML ранжирования (сравнение с BM25-топ-5):")

        print(f" Precision: {precision:.4f}, Recall: {recall:.4f}, nDCG: {ndcg_val:.4f}")



if __name__ == "__main__":

    run_ranking()

