import os
import re
import json
from collections import defaultdict
from typing import Dict, List, Tuple
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import nltk
import time

class SearchEngine:
    def __init__(self, folder: str = "Lab4/Docs", index_file: str = "Lab4/inverted_index.json"):
        self.folder = folder
        self.index_file = index_file
        self.stemmer = SnowballStemmer("russian")
        self.stop_words = set(stopwords.words('russian'))
        self.inverted_index = None
        self.documents = None
        
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')

    def read_documents(self) -> Dict[str, str]:
        documents = {}
        try:
            for filename in os.listdir(self.folder):
                if filename.endswith(".txt"):
                    filepath = os.path.join(self.folder, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        text = f.read().lower()
                        text = re.sub(r'[^\w\s]', '', text)
                        documents[filename] = text
        except FileNotFoundError:
            print(f"Папка {self.folder} не найдена")
            return {}
        except Exception as e:
            print(f"Ошибка при чтении файлов: {e}")
            return {}
        return documents

    def tokenize_and_stem(self, text: str) -> List[str]:
        """Токенизация и стемминг текста."""
        tokens = re.findall(r'\b\w+\b', text)
        return [self.stemmer.stem(token) for token in tokens if token not in self.stop_words]

    def build_inverted_index(self, documents: Dict[str, str]) -> Dict:
        """Построение инвертированного индекса."""
        inverted_index = defaultdict(lambda: defaultdict(lambda: {"frequency": 0, "positions": []}))
        
        for doc_id, text in documents.items():
            tokens = self.tokenize_and_stem(text)
            for pos, token in enumerate(tokens):
                inverted_index[token][doc_id]["frequency"] += 1
                inverted_index[token][doc_id]["positions"].append(pos)
        
        try:
            with open(self.index_file, "w", encoding="utf-8") as f:
                json.dump(dict(inverted_index), f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении индекса: {e}")
        
        self.inverted_index = inverted_index
        return inverted_index

    def search_words(self, query: str) -> Dict[str, List[Tuple[str, int, List[int]]]]:
        """Поиск отдельных слов с использованием инвертированного индекса."""
        if not self.inverted_index:
            return {}
            
        query_tokens = self.tokenize_and_stem(query)
        result_docs = defaultdict(list)
        
        for token in query_tokens:
            if token in self.inverted_index:
                for doc_id, data in self.inverted_index[token].items():
                    result_docs[doc_id].append((token, data["frequency"], data["positions"]))
        
        return dict(result_docs)

    def brute_force_search_words(self, query: str) -> Dict[str, List[Tuple[str, int, List[int]]]]:
        """Поиск отдельных слов методом перебора."""
        if not self.documents:
            return {}
            
        query_tokens = self.tokenize_and_stem(query)
        result_docs = defaultdict(list)
        
        for doc_id, text in self.documents.items():
            doc_tokens = self.tokenize_and_stem(text)
            for token in query_tokens:
                frequency = 0
                positions = []
                for pos, doc_token in enumerate(doc_tokens):
                    if doc_token == token:
                        frequency += 1
                        positions.append(pos)
                if frequency > 0:
                    result_docs[doc_id].append((token, frequency, positions))
        
        return dict(result_docs)

    def search_phrase(self, phrase: str) -> List[Tuple[str, Dict[str, List[int]]]]:
        if not self.inverted_index:
            return []
            
        phrase_tokens = self.tokenize_and_stem(phrase)
        if not phrase_tokens:
            return []
            
        first_word, *rest_words = phrase_tokens
        if first_word not in self.inverted_index:
            return []
        
        candidate_docs = set(self.inverted_index[first_word].keys())
        for word in rest_words:
            if word not in self.inverted_index:
                return []
            candidate_docs &= set(self.inverted_index[word].keys())
        
        matching_docs = []
        for doc_id in candidate_docs:
            positions = [self.inverted_index[word][doc_id]["positions"] for word in phrase_tokens]
            for pos in positions[0]:
                if all(pos + i in positions[i] for i in range(len(positions))):
                    word_positions = {phrase_tokens[i]: [pos + i] for i in range(len(phrase_tokens))}
                    matching_docs.append((doc_id, word_positions))
                    break
        
        return matching_docs

    def brute_force_search(self, phrase: str) -> List[Tuple[str, Dict[str, List[int]]]]:
        if not self.documents:
            return []
            
        phrase_tokens = self.tokenize_and_stem(phrase)
        if not phrase_tokens:
            return []
            
        matching_docs = []
        for doc_id, text in self.documents.items():
            doc_tokens = self.tokenize_and_stem(text)
            for i in range(len(doc_tokens) - len(phrase_tokens) + 1):
                if doc_tokens[i:i + len(phrase_tokens)] == phrase_tokens:
                    word_positions = {phrase_tokens[j]: [i + j] for j in range(len(phrase_tokens))}
                    matching_docs.append((doc_id, word_positions))
                    break
        
        return matching_docs

def main():
    search_engine = SearchEngine()

    search_engine.documents = search_engine.read_documents()
    if not search_engine.documents:
        print("Нет документов для обработки")
        return
        
    _ = search_engine.build_inverted_index(search_engine.documents)

    query = "Эльфийский хлеб"
            
    # Поиск отдельных слов с инвертированным индексом
    start_time = time.perf_counter()
    word_index_results = search_engine.search_words(query)
    word_index_time = time.perf_counter() - start_time
        
    # Поиск отдельных слов перебором
    start_time = time.perf_counter()
    word_brute_results = search_engine.brute_force_search_words(query)
    word_brute_time = time.perf_counter() - start_time
        
    # Поиск фразы с инвертированным индексом
    start_time = time.perf_counter()
    phrase_index_results = search_engine.search_phrase(query)
    phrase_index_time = time.perf_counter() - start_time
        
    # Поиск фразы перебором
    start_time = time.perf_counter()
    phrase_brute_results = search_engine.brute_force_search(query)
    phrase_brute_time = time.perf_counter() - start_time
        
    print("\n" + "="*60)
    print(f"Результаты поиска для запроса: '{query}'")
    print("="*60)
        
    # Поиск слов с индексом
    print("\n\033[1mРезультаты поиска (инвертированный индекс):\033[0m")
    if word_index_results:
        for doc, tokens in word_index_results.items():
            token_info = ", ".join([f"{t[0]} (частота: {t[1]}, позиции: {t[2]})" for t in tokens])
            if len(tokens) > 1: print(f"Слово: {token_info}, \nдокументы: {doc}")
        print("-" * 60)
        for doc, tokens in word_index_results.items():
            token_info = ", ".join([f"{t[0]} (частота: {t[1]}, позиции: {t[2]})" for t in tokens])
            if len(tokens) == 1: print(f"Слово: {token_info}, \nдокументы: {doc}")
        print("-" * 60)
    else:
        print("  Ничего не найдено")
    print(f"  \033[3mВремя выполнения: {word_index_time:.6f} сек\033[0m")
        
    # Поиск фразы с индексом
    print("\n\033[1mРезультаты поиска фразы целиком (инвертированный индекс):\033[0m")
    if phrase_index_results:
        for doc, positions in phrase_index_results:
            pos_info = ", ".join([f"{word}: {pos}" for word, pos in positions.items()])
            print(f"  Документ: {doc}")
            print(f"  Позиции слов: {pos_info}")
        print("-" * 60)
    else:
        print("  Фраза не найдена")
    print(f"  \033[3mВремя выполнения: {phrase_index_time:.6f} сек\033[0m")

    print("\n" + "="*60)

    # Поиск слов перебором
    print("\n\033[1mРезультаты поиска отдельных слов (перебор):\033[0m")
    if word_brute_results:
        for doc, tokens in word_brute_results.items():
            token_info = ", ".join([f"{t[0]} (частота: {t[1]}, позиции: {t[2]})" for t in tokens])
            if len(tokens) > 1: print(f"Слово: {token_info}, \nдокументы: {doc}")
        print("-" * 60)
        for doc, tokens in word_brute_results.items():
            token_info = ", ".join([f"{t[0]} (частота: {t[1]}, позиции: {t[2]})" for t in tokens])
            if len(tokens) == 1: print(f"Слово: {token_info}, \nдокументы: {doc}")
        print("\n" + "-"*60)
    else:
        print("  Ничего не найдено")
    print(f"  \033[3mВремя выполнения: {word_brute_time:.6f} сек\033[0m")
        
    # Поиск фразы перебором
    print("\n\033[1mРезультаты поиска фразы целиком (перебор):\033[0m")
    if phrase_brute_results:
        for doc, pos in phrase_brute_results:
            pos_info = ", ".join([f"{word}: {pos}" for word, pos in positions.items()])
            print(f"  Документ: {doc}")
            print(f"  Позиции слов: {pos_info}")
        print("-" * 60)
    else:
        print("  Фраза не найдена")
    print(f"  \033[3mВремя выполнения: {phrase_brute_time:.6f} сек\033[0m")
        
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
