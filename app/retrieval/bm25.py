from math import log
from typing import List, Sequence

def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in text.split()]

class BM25Okapi:
    def __init__(self, corpus: Sequence[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus = [ _tokenize(doc) for doc in corpus ]
        self.doc_lens = [ len(doc) for doc in self.corpus ]
        self.avgdl = sum(self.doc_lens) / len(self.doc_lens) if self.doc_lens else 0.0
        # term frequencies per doc
        self.tf = []
        self.df = {}
        for doc in self.corpus:
            tf_doc = {}
            seen = set()
            for w in doc:
                tf_doc[w] = tf_doc.get(w, 0) + 1
            self.tf.append(tf_doc)
            for w in tf_doc:
                if w not in seen:
                    self.df[w] = self.df.get(w, 0) + 1
                    seen.add(w)
        self.N = len(self.corpus)

    def get_scores(self, query: str) -> List[float]:
        q = _tokenize(query)
        scores = [0.0] * self.N
        for i, doc_tf in enumerate(self.tf):
            dl = self.doc_lens[i] or 1
            for w in q:
                if w not in doc_tf:
                    continue
                n_qi = self.df.get(w, 0) or 1
                idf = log((self.N - n_qi + 0.5) / (n_qi + 0.5) + 1.0)
                freq = doc_tf[w]
                denom = freq + self.k1 * (1 - self.b + self.b * dl / (self.avgdl or 1))
                score = idf * (freq * (self.k1 + 1)) / (denom or 1)
                scores[i] += score
        return scores
