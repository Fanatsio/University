import os
import json
import numpy as np
import pandas as pd
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, precision_recall_fscore_support
from collections import defaultdict

DATA_DIR = "wiki_docs"
INDEX_FILE = "inverted_index.json"
LINKS_FILE = "links.json"


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


documents_split = {}
for file, content in documents.items():
    documents_split[file] = content.split()


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
            score = 0
            for term in query_terms:
                if term in self.index and doc in self.index[term]:
                    freq = self.index[term][doc]
                    score += self._bm25_term_score(term, freq, doc)
            scores[doc] = score
        return scores
    
    def _bm25_term_score(self, term, freq, doc):

        doc_freq = len(self.index.get(term, {}))

        idf = math.log((len(self.docs) - doc_freq + 0.5) / (doc_freq + 0.5) + 1)

        tf = (freq * (self.k1 + 1)) / (freq + self.k1 * (1 - self.b + self.b * (self.doc_lengths[doc] / self.avg_doc_length)))
        return idf * tf

bm25 = BM25(inverted_index, documents_split)

def prepare_training_data(query_list=None):
    if query_list is None:
        query_list = [
            "поиск",
            "состояние",
            "цифровой",
            "Валдай"
        ]

    dataset = []

    for query in query_list:
        clean_query = query.lower().strip()
        query_terms = [term for term in clean_query.split() if term]


        bm25_scores = bm25.score(clean_query)

        max_bm25 = max(bm25_scores.values()) if bm25_scores else 1

        for doc_id in all_doc_ids:
            if doc_id in documents:
                doc_content = documents[doc_id].lower()

                bm25_score = bm25_scores.get(doc_id, 0) / max_bm25 if max_bm25 > 0 else 0

                term_coverage = (
                    sum(1 for term in query_terms if term in doc_content) / len(query_terms)
                    if query_terms else 0
                )

                doc_words = doc_content.split()
                positions = [
                    i for i, word in enumerate(doc_words) if word in query_terms
                ]
                position_score = 1 - min(min(positions) / 100, 1) if positions else 0

                title = links_mapping.get(doc_id, {}).get('title', '').lower()
                title_match = (
                    sum(1 for term in query_terms if term in title) / len(query_terms)
                    if query_terms else 0
                )

                weighted_score = (
                    0.5 * bm25_score +
                    0.2 * term_coverage +
                    0.2 * title_match +
                    0.1 * position_score
                )

                if weighted_score > 0.8:
                    relevance = 5
                elif weighted_score > 0.6:
                    relevance = 4
                elif weighted_score > 0.4:
                    relevance = 3
                elif weighted_score > 0.2:
                    relevance = 2
                elif weighted_score > 0:
                    relevance = 1
                else:
                    relevance = 0

                features = extract_features(clean_query, doc_id)

                dataset.append({
                    'query': clean_query,
                    'doc_id': doc_id,
                    'features': features,
                    'relevance': relevance,
                    'score_components': {
                        'bm25': bm25_score,
                        'term_coverage': term_coverage,
                        'title_match': title_match,
                        'position_score': position_score,
                        'weighted_score': weighted_score
                    }
                })

    return dataset

def save_dataset(dataset, filename='training_data.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

def extract_features(query, doc_id):
    doc_text = documents[doc_id]
    query_terms = query.lower().split()
    
    bm25_values = []
    for term in query_terms:
        bm25_value = 0
        if term in inverted_index and doc_id in inverted_index[term]:
            freq = inverted_index[term][doc_id]
            bm25_value = bm25._bm25_term_score(term, freq, doc_id)
        bm25_values.append(bm25_value)
    

    doc_words = doc_text.lower().split()
    positions = []
    for term in query_terms:
        term_positions = [i for i, word in enumerate(doc_words) if word == term]
        if term_positions:
            positions.extend(term_positions)
    
    return {
        'bm25_sum': sum(bm25_values),
        'bm25_avg': np.mean(bm25_values) if bm25_values else 0,
        'bm25_max': max(bm25_values) if bm25_values else 0,
        

        'doc_length': len(doc_words),
        
        'min_position': min(positions) if positions else len(doc_words),
        'avg_position': np.mean(positions) if positions else len(doc_words),

        'term_count': sum(1 for term in query_terms if term in doc_text.lower()),
        'term_ratio': sum(1 for term in query_terms if term in doc_text.lower()) / len(query_terms) if query_terms else 0
    }

def train_ranking_model(dataset, model_type='logistic'):
    X = pd.DataFrame([item['features'] for item in dataset])
    y = np.array([item['relevance'] for item in dataset])
    
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    if model_type == 'logistic':
        model = LogisticRegression(max_iter=1000)
    elif model_type == 'random_forest':
        model = RandomForestClassifier(n_estimators=100)
    elif model_type == 'gbdt':
        model = GradientBoostingClassifier(n_estimators=100)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    
    model.fit(X_train, y_train)
    
    train_preds = model.predict(X_train)
    val_preds = model.predict(X_val)
    
    metrics = {
        'train_precision': precision_score(y_train, train_preds, average='weighted', zero_division=0),
        'train_recall': recall_score(y_train, train_preds, average='weighted', zero_division=0),
        'val_precision': precision_score(y_val, val_preds, average='weighted', zero_division=0),
        'val_recall': recall_score(y_val, val_preds, average='weighted', zero_division=0),
    }
    
    return model, metrics

def search_with_ml_ranking(query, model, top_n=10):
    candidates = [doc_id for doc_id in all_doc_ids if doc_id in documents]
    candidate_features = [extract_features(query, doc_id) for doc_id in candidates]

    X_candidates = pd.DataFrame(candidate_features)
    relevance_classes = model.predict(X_candidates)
    
    results = list(zip(candidates, relevance_classes))
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    return sorted_results[:top_n]


def main():
    queries = [
        "поиск",
        "состояние",
        "цифровой",
        "Валдай"
    ]

    print("Подготовка данных...")
    dataset = prepare_training_data(query_list=queries)

    print("Обучение модели...")
    model, metrics = train_ranking_model(dataset, model_type='gbdt')
    print(f"Метрики модели (обучение): {metrics}")

    for query in queries:
        print(f"\n=== Запрос: {query} ===")


        bm25_results_dict = bm25.score(query)
        bm25_results_sorted = sorted(bm25_results_dict.items(), key=lambda x: x[1], reverse=True)[:10]

        print("\n[BM25 результаты]")
        for doc_id, score in bm25_results_sorted:
            title = links_mapping.get(doc_id, {}).get('title', 'Неизвестно')
            print(f"  - {title} (Оценка BM25: {score:.4f})")

        print("\n[ML результаты]")
        ml_results = search_with_ml_ranking(query, model, top_n=10)
        for doc_id, rel_class in ml_results:
            title = links_mapping.get(doc_id, {}).get('title', 'Неизвестно')
            print(f"  - {title} (Предсказанная релевантность: {rel_class})")


        true_relevance = [item['relevance'] for item in dataset if item['query'] == query]
        predicted_relevance = []
        candidate_docs = [item['doc_id'] for item in dataset if item['query'] == query]

        for doc_id in candidate_docs:
            feats = extract_features(query, doc_id)
            pred = model.predict(pd.DataFrame([feats]))[0]
            predicted_relevance.append(pred)

     
        true_binary = [1 if rel > 0 else 0 for rel in true_relevance]
        pred_binary = [1 if rel > 0 else 0 for rel in predicted_relevance]

        precision, recall, f1, _ = precision_recall_fscore_support(
            true_binary, pred_binary, average='binary', zero_division=0
        )

        print(f"\n[Метрики ML для запроса '{query}']")
        print(f" Precision: {precision:.4f}")
        print(f" Recall:    {recall:.4f}")
        print(f" F1-score:  {f1:.4f}")


        dataset = prepare_training_data(query_list=queries)
        save_dataset(dataset, filename='training_data.json')

if __name__ == "__main__":
    main()