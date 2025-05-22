import os
import json
import numpy as np
import pandas as pd
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

DATA_DIR = "wiki_docs"
INDEX_FILE = "inverted_index.json"
LINKS_FILE = "links.json"

# Загрузка данных
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    inverted_index = json.load(f)
with open(LINKS_FILE, "r", encoding="utf-8") as f:
    links_mapping = json.load(f)

documents = {}
for file in os.listdir(DATA_DIR):
    if file.endswith(".txt"):
        file_path = os.path.join(DATA_DIR, file)
        with open(file_path, "r", encoding="utf-8") as f:
            documents[file] = f.read()

documents_split = {file: content.split() for file, content in documents.items()}
all_doc_ids = list(documents.keys())

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
            score = sum(self._bm25_term_score(term, self.index[term][doc], doc)
                        for term in query_terms if term in self.index and doc in self.index[term])
            scores[doc] = score
        return scores

    def _bm25_term_score(self, term, freq, doc):
        doc_freq = len(self.index.get(term, {}))
        idf = math.log((len(self.docs) - doc_freq + 0.5) / (doc_freq + 0.5) + 1)
        tf = (freq * (self.k1 + 1)) / (freq + self.k1 * (1 - self.b + self.b * (self.doc_lengths[doc] / self.avg_doc_length)))
        return idf * tf

bm25 = BM25(inverted_index, documents_split)

# Подготовка данных
def prepare_training_data(query_list):
    dataset = []
    for query in query_list:
        bm25_scores = bm25.score(query)
        max_bm25 = max(bm25_scores.values()) if bm25_scores else 1
        for doc_id in all_doc_ids:
            doc_content = documents[doc_id].lower()
            term_coverage = sum(term in doc_content for term in query.lower().split()) / len(query.split())
            weighted_score = 0.7 * (bm25_scores.get(doc_id, 0) / max_bm25) + 0.3 * term_coverage
            relevance = int(weighted_score * 5)
            features = extract_features(query, doc_id)
            dataset.append({'query': query, 'doc_id': doc_id, 'features': features, 'relevance': relevance})
    return dataset

# Извлечение признаков
def extract_features(query, doc_id):
    query_terms = query.lower().split()
    bm25_values = [bm25._bm25_term_score(term, inverted_index[term][doc_id], doc_id)
                   if term in inverted_index and doc_id in inverted_index[term] else 0
                   for term in query_terms]
    doc_words = documents[doc_id].lower().split()
    positions = [i for term in query_terms for i, word in enumerate(doc_words) if word == term]
    return {
        'bm25_sum': sum(bm25_values), 'bm25_avg': np.mean(bm25_values), 'bm25_max': max(bm25_values),
        'doc_length': len(doc_words), 'min_position': min(positions, default=len(doc_words)),
        'avg_position': np.mean(positions) if positions else len(doc_words),
        'term_count': sum(term in doc_words for term in query_terms),
        'term_ratio': sum(term in doc_words for term in query_terms) / len(query_terms),
    }

# Обучение модели
def train_ranking_model(dataset, model_type='gbdt'):
    X = pd.DataFrame([item['features'] for item in dataset])
    y = np.array([item['relevance'] for item in dataset])
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    models = {'logistic': LogisticRegression(max_iter=1000),
              'random_forest': RandomForestClassifier(),
              'gbdt': GradientBoostingClassifier()}
    model = models[model_type]
    model.fit(X_train, y_train)
    return model

# Оценка по запросам
def evaluate_model(query_list, model):
    for query in query_list:
        dataset = prepare_training_data([query])
        X = pd.DataFrame([item['features'] for item in dataset])
        y_true = np.array([item['relevance'] for item in dataset])
        y_pred = model.predict(X)
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        print(f"Запрос: '{query}'\n Precision: {precision:.3f}, Recall: {recall:.3f}, F1: {f1:.3f}\n")

def main():
    queries = ["поисковая система", "нелинейный сюжет", "цифровой звук", "Валдай"]
    dataset = prepare_training_data(queries)
    model = train_ranking_model(dataset, model_type='gbdt')
    evaluate_model(queries, model)

if __name__ == "__main__":
    main()