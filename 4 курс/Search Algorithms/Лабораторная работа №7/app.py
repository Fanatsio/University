import os
import time
import pickle
import json
from flask import Flask, request, render_template, redirect, make_response
import numpy as np
from crawler import WebCrawler
from indexer import Indexer
from ranker import Ranker

app = Flask(__name__)

# Configuration
MAX_DEPTH = 2
MAX_PAGES = 150  # Increased to 150 pages
PER_PAGE = 20
SEED_URLS = [
    "https://ru.wikipedia.org/wiki/Мастер_и_Маргарита",
    "https://ru.wikipedia.org/wiki/Кот",
    "https://ru.wikipedia.org/wiki/Поисковая_система",
    "https://ru.wikipedia.org/wiki/Поисковик",
    "https://ru.wikipedia.org/wiki/Монреаль",
    "https://ru.wikipedia.org/wiki/Google",
    "https://ru.wikipedia.org/wiki/Яндекс",
    "https://ru.wikipedia.org/wiki/PageRank",
    "https://ru.wikipedia.org/wiki/Информационный_поиск",
    "https://ru.wikipedia.org/wiki/Всемирная_паутина"
]

DATA = {
    "docs": {},
    "inv": {},
    "dl": {},
    "pr": {},
    "imp": {},
    "clk": {},
    "dw": {},
    "bc": {}
}
SESSION_START = {}
SESSION_URL = {}

def load_data():
    """Load search data from pickle file (fallback, optional)."""
    if os.path.exists("search_data.pkl"):
        try:
            with open("search_data.pkl", "rb") as f:
                return pickle.load(f)
        except (pickle.PickleError, FileNotFoundError):
            return None
    return None

def save_data():
    """Save search data to separate text files in search_data/ directory."""
    output_dir = "search_data"
    os.makedirs(output_dir, exist_ok=True)

    # Save crawled pages
    with open(os.path.join(output_dir, "crawled_pages.txt"), "w", encoding="utf-8") as f:
        for url, data in DATA["docs"].items():
            f.write(f"URL: {url}\n")
            f.write(f"Title: {data['title']}\n")
            f.write(f"Text: {data['text'][:500]}...\n")  # Truncate for brevity
            f.write("-" * 80 + "\n")

    # Save inverted index
    with open(os.path.join(output_dir, "inverted_index.txt"), "w", encoding="utf-8") as f:
        for term, postings in DATA["inv"].items():
            f.write(f"Term: {term}\n")
            f.write("Postings: ")
            for posting in postings:
                url = posting[0]  # First element is URL
                freq = posting[1]  # Second element is frequency
                f.write(f"({url}, {freq}) ")
            f.write("\n" + "-" * 80 + "\n")

    # Save document lengths
    with open(os.path.join(output_dir, "document_lengths.txt"), "w", encoding="utf-8") as f:
        for url, length in DATA["dl"].items():
            f.write(f"URL: {url}\n")
            f.write(f"Length: {length}\n")
            f.write("-" * 80 + "\n")

    # Save PageRank scores
    with open(os.path.join(output_dir, "pagerank_scores.txt"), "w", encoding="utf-8") as f:
        for url, score in DATA["pr"].items():
            f.write(f"URL: {url}\n")
            f.write(f"PageRank: {score}\n")
            f.write("-" * 80 + "\n")

    # Save impressions
    with open(os.path.join(output_dir, "impressions.txt"), "w", encoding="utf-8") as f:
        for url, count in DATA["imp"].items():
            f.write(f"URL: {url}\n")
            f.write(f"Impressions: {count}\n")
            f.write("-" * 80 + "\n")

    # Save clicks
    with open(os.path.join(output_dir, "clicks.txt"), "w", encoding="utf-8") as f:
        for url, count in DATA["clk"].items():
            f.write(f"URL: {url}\n")
            f.write(f"Clicks: {count}\n")
            f.write("-" * 80 + "\n")

    # Save dwell time
    with open(os.path.join(output_dir, "dwell_times.txt"), "w", encoding="utf-8") as f:
        for url, time_spent in DATA["dw"].items():
            f.write(f"URL: {url}\n")
            f.write(f"Dwell Time: {time_spent}\n")
            f.write("-" * 80 + "\n")

    # Save bounce counts
    with open(os.path.join(output_dir, "bounce_counts.txt"), "w", encoding="utf-8") as f:
        for url, count in DATA["bc"].items():
            f.write(f"URL: {url}\n")
            f.write(f"Bounce Count: {count}\n")
            f.write("-" * 80 + "\n")

def initialize_data():
    """Initialize search data by crawling and indexing."""
    crawler = WebCrawler(max_depth=MAX_DEPTH, max_pages=MAX_PAGES)
    docs_content, adj_list = crawler.crawl(SEED_URLS)
    
    indexer = Indexer()
    inv, dl = indexer.build_inverted_index(docs_content)
    mat, urls, _ = indexer.build_adjacency_matrix(adj_list)
    
    ranker = Ranker()
    pr_vals = ranker.pagerank(mat)
    pr_dict = {u: pr_vals[i] for i, u in enumerate(urls)}
    
    DATA.update({
        "docs": docs_content,
        "inv": inv,
        "dl": dl,
        "pr": pr_dict,
        "imp": {},
        "clk": {},
        "dw": {},
        "bc": {}
    })
    save_data()

@app.route("/")
def index():
    """Render the main search page."""
    return render_template("index.html")

@app.route("/search")
def search():
    """Handle search queries and display results."""
    query = request.args.get("q", "").strip()
    if not query:
        return render_template("index.html", error="Пустой запрос")

    try:
        page = int(request.args.get("page", "1"))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    indexer = Indexer()
    ranker = Ranker()
    tokens = indexer.tokenize_lemma(query)
    results = ranker.combined_ranking(
        tokens, DATA["inv"], DATA["dl"], DATA["docs"], DATA["pr"],
        DATA["imp"], DATA["clk"], DATA["dw"], DATA["bc"]
    )

    for result in results:
        DATA["imp"][result["url"]] = DATA["imp"].get(result["url"], 0) + 1

    total_results = len(results)
    total_pages = (total_results + PER_PAGE - 1) // PER_PAGE
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    subset = results[start:end]

    # Add snippets to results
    for result in subset:
        result["snippet"] = ranker.generate_snippet(query, result["url"], DATA["docs"])

    save_data()
    return render_template(
        "index.html",
        query=query,
        results=subset,
        page=page,
        total_pages=total_pages,
        total_results=total_results,
        per_page=PER_PAGE
    )

@app.route("/click")
def click():
    """Handle click events and redirect to target URL."""
    target = request.args.get("target", "")
    query = request.args.get("q", "")
    if not target:
        return render_template("index.html", error="Ошибка: нет ссылки")

    DATA["clk"][target] = DATA["clk"].get(target, 0) + 1
    s_id = str(int(time.time() * 1000)) + str(np.random.randint(100000))
    SESSION_START[s_id] = time.time()
    SESSION_URL[s_id] = target

    resp = make_response(redirect(target))
    resp.set_cookie("session_id", s_id)
    save_data()
    return resp

@app.route("/return_to_results")
def return_to_results():
    """Handle return from clicked link and update metrics."""
    s_id = request.cookies.get("session_id")
    if s_id in SESSION_START:
        delta = time.time() - SESSION_START[s_id]
        doc_url = SESSION_URL[s_id]
        DATA["dw"][doc_url] = DATA["dw"].get(doc_url, 0) + delta
        if delta < 5:
            DATA["bc"][doc_url] = DATA["bc"].get(doc_url, 0) + 1
        del SESSION_START[s_id]
        del SESSION_URL[s_id]
        save_data()

    return render_template("index.html", error="Вы вернулись на результаты")

if __name__ == "__main__":
    loaded_data = load_data()
    if loaded_data:
        DATA.update(loaded_data)
    else:
        initialize_data()
    app.run(debug=True, port=5000)