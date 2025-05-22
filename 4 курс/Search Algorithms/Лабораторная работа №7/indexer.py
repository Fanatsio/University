from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import numpy as np

class Indexer:
    """Builds inverted index and adjacency matrix for search."""
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('russian'))

    def tokenize_lemma(self, text):
        """Tokenize and lemmatize text."""
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [re.sub(r'[^а-яёa-z]+', '', w) for w in tokens]
        tokens = [w for w in tokens if w and w not in self.stop_words]
        return [self.lemmatizer.lemmatize(w) for w in tokens]

    def build_inverted_index(self, docs_content):
        """Create inverted index and document lengths."""
        inv_index = {}
        doc_lengths = {}
        for url, data in docs_content.items():
            toks = self.tokenize_lemma(data["text"])
            doc_lengths[url] = len(toks)
            for pos, token in enumerate(toks):
                if token not in inv_index:
                    inv_index[token] = {}
                if url not in inv_index[token]:
                    inv_index[token][url] = {"freq": 0, "positions": []}
                inv_index[token][url]["freq"] += 1
                inv_index[token][url]["positions"].append(pos)
        return inv_index, doc_lengths

    def build_adjacency_matrix(self, adj_list):
        """Create adjacency matrix for PageRank."""
        urls = list(adj_list.keys())
        url_to_id = {u: i for i, u in enumerate(urls)}
        n = len(urls)
        matrix = np.zeros((n, n), dtype=float)

        for u in urls:
            i = url_to_id[u]
            outlinks = adj_list[u]
            if not outlinks:
                matrix[i, :] = 1.0 / n
            else:
                for v in outlinks:
                    if v in url_to_id:
                        j = url_to_id[v]
                        matrix[i, j] = 1.0
        for i in range(n):
            row_sum = np.sum(matrix[i, :])
            if row_sum > 0:
                matrix[i, :] /= row_sum
            else:
                matrix[i, :] = 1.0 / n
        return matrix, urls, url_to_id