import numpy as np
import math
import re

class Ranker:
    """Handles ranking of search results using BM25 and PageRank."""
    
    def __init__(self, d=0.85, tol=1e-6, max_iter=100, k1=1.2, b=0.75):
        self.d = d
        self.tol = tol
        self.max_iter = max_iter
        self.k1 = k1
        self.b = b

    def pagerank(self, matrix):
        """Compute PageRank scores."""
        n = matrix.shape[0]
        pr = np.ones(n) / n
        for _ in range(self.max_iter):
            new_pr = (1 - self.d) / n + self.d * np.dot(matrix.T, pr)
            if np.linalg.norm(new_pr - pr, 1) < self.tol:
                pr = new_pr
                break
            pr = new_pr
        return pr

    def compute_idf(self, inverted_index, total_docs):
        """Compute IDF for terms."""
        idf_dict = {}
        for term, posting in inverted_index.items():
            df = len(posting)
            val = math.log((total_docs - df + 0.5) / (df + 0.5) + 1)
            idf_dict[term] = val
        return idf_dict

    def bm25_score(self, query_tokens, url, inv_index, doc_lengths, idf_dict, avgdl):
        """Calculate BM25 score for a document."""
        score = 0.0
        dl = doc_lengths[url]
        for t in query_tokens:
            if t not in inv_index or url not in inv_index[t]:
                continue
            freq = inv_index[t][url]["freq"]
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * (dl / avgdl))
            score += idf_dict.get(t, 0) * (numerator / denominator)
        return score

    def combined_score(self, url, bm25_val, pr_val, impressions, clicks, dwell, bounce_count):
        """Combine BM25, PageRank, and user interaction metrics."""
        real_ctr = clicks.get(url, 0) / impressions.get(url, 1) if impressions.get(url, 0) > 0 else 0
        return (bm25_val + 0.5 * pr_val + 2 * real_ctr + 
                0.01 * dwell.get(url, 0) - bounce_count.get(url, 0))

    def generate_snippet(self, query, url, docs_content):
        """Generate a snippet for the document containing query terms."""
        text = docs_content[url]["text"].lower()
        query_terms = query.lower().split()
        snippet_length = 150

        # Find the first occurrence of any query term
        best_snippet = ""
        best_position = len(text)
        for term in query_terms:
            match = re.search(rf'\b{re.escape(term)}\b', text)
            if match and match.start() < best_position:
                best_position = match.start()
                best_snippet = text[max(0, best_position - 50):best_position + 100]

        # Truncate snippet to desired length
        if len(best_snippet) > snippet_length:
            best_snippet = best_snippet[:snippet_length] + "..."
        elif not best_snippet:
            best_snippet = text[:snippet_length] + ("..." if len(text) > snippet_length else "")

        return best_snippet

    def combined_ranking(self, query_tokens, inv_index, doc_lengths, docs_content, pr_dict, 
                        impressions, clicks, dwell, bounce_count):
        """Rank documents based on combined scores."""
        candidates = set()
        for t in query_tokens:
            if t in inv_index:
                candidates |= set(inv_index[t].keys())
        if not candidates:
            return []

        total_docs = len(docs_content)
        idf_dict = self.compute_idf(inv_index, total_docs)
        avgdl = sum(doc_lengths.values()) / total_docs if total_docs > 0 else 1
        results = []

        for url in candidates:
            bm25_val = self.bm25_score(query_tokens, url, inv_index, doc_lengths, idf_dict, avgdl)
            pr_val = pr_dict.get(url, 0)
            final_val = self.combined_score(url, bm25_val, pr_val, impressions, clicks, dwell, bounce_count)
            results.append({"url": url, "title": docs_content[url]["title"], "score": final_val})

        return sorted(results, key=lambda x: x["score"], reverse=True)