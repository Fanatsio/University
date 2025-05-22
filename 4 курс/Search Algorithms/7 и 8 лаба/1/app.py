import os
import json
import math
import numpy as np
import networkx as nx
from collections import defaultdict
from flask import Flask, request, render_template

W1, W2 = 0.3, 0.7

INDEX_FILE = "inverted_index.json"
LINKS_FILE = "links.json"
DATA_DIR = "wiki_docs"

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    inverted_index = json.load(f)

with open(LINKS_FILE, "r", encoding="utf-8") as f:
    links_mapping = json.load(f)

documents = {}
for file in os.listdir(DATA_DIR):
    file_path = os.path.join(DATA_DIR, file)
    with open(file_path, "r", encoding="utf-8") as f:
        documents[file] = f.read().split()

class BM25:
    def __init__(self, index, docs):
        self.index = index  
        self.docs = docs
        self.doc_lengths = {doc: len(words) for doc, words in docs.items()}
        self.avg_doc_length = sum(self.doc_lengths.values()) / len(docs)
        self.k1 = 1.5
        self.b = 0.75

    def score(self, query):
        query_terms = query.lower().split()
        scores = {}

        for doc in self.docs.keys():
            score = 0
            for term in query_terms:
                if term in self.index and doc in self.index[term]:
                    freq = self.index[term][doc] 
                    score += self._bm25_term_score(freq, doc)
            scores[doc] = score
        return scores

    def _bm25_term_score(self, freq, doc):
        idf = math.log((len(self.docs) - len(self.index.get(doc, {})) + 0.5) / (len(self.index.get(doc, {})) + 0.5) + 1)
        tf = (freq * (self.k1 + 1)) / (freq + self.k1 * (1 - self.b + self.b * (self.doc_lengths[doc] / self.avg_doc_length)))
        return idf * tf

bm25 = BM25(inverted_index, documents)

def compute_pagerank(links, alpha=0.85):
    G = nx.DiGraph(links)
    return nx.pagerank(G, alpha=alpha)

links_graph = {doc: [f"page_{i}.txt" for i in range(5)] for doc in documents}
pagerank_scores = compute_pagerank(links_graph)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return render_template("index.html", results=[])

    query_terms = query.split()  # Разбиваем запрос на слова
    bm25_scores = bm25.score(query)  # Считаем BM25

    relevant_docs = {doc: score for doc, score in bm25_scores.items() if score > 0}

    if not relevant_docs:
        return render_template("index.html", results=[])

    final_scores = {
        doc: W1 * bm25_scores[doc] + W2 * pagerank_scores.get(doc, 0)
        for doc in relevant_docs
    }

    sorted_results = [
        (links_mapping[doc]["title"], links_mapping[doc]["url"], score)
        for doc, score in sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        if doc in links_mapping
    ]

    return render_template("index.html", results=sorted_results)


if __name__ == "__main__":
    app.run( port=8080, debug=True)
