
import math
import re
from collections import defaultdict
from typing import List, Dict, Tuple

class SimpleTfidfRetriever:
    def __init__(self, docs: List[str]):
        self.docs = docs
        self.vocab_df = defaultdict(int)
        self.doc_vecs = []
        for d in docs:
            tokens = set(re.findall(r'[A-Za-z]{3,}', d.lower()))
            for t in tokens:
                self.vocab_df[t] += 1
        for d in docs:
            self.doc_vecs.append(self._tfidf(d))

    def _tfidf(self, text: str) -> Dict[str, float]:
        counts = defaultdict(int)
        tokens = [w for w in re.findall(r'[A-Za-z]{3,}', text.lower())]
        for w in tokens:
            counts[w] += 1
        vec = {}
        N = len(self.docs)
        for w, c in counts.items():
            idf = math.log((1 + N) / (1 + self.vocab_df[w])) + 1
            vec[w] = c * idf
        return vec

    @staticmethod
    def _cosine(a: Dict[str, float], b: Dict[str, float]) -> float:
        keys = set(a) | set(b)
        dot = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
        na = math.sqrt(sum(v*v for v in a.values()))
        nb = math.sqrt(sum(v*v for v in b.values()))
        return dot / (na * nb + 1e-9)

    def query(self, q: str, top_k: int = 5) -> List[Tuple[int, float]]:
        qv = self._tfidf(q)
        scored = [(i, self._cosine(qv, dv)) for i, dv in enumerate(self.doc_vecs)]
        return sorted(scored, key=lambda x: x[1], reverse=True)[:top_k]
