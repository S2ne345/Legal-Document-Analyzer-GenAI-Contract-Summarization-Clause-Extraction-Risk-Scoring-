
from collections import defaultdict
import math
import re

# Simple TextRank-like summarizer without external deps

def sentence_split(text: str):
    parts = re.split(r'(?:\.|\?|!)\s+', text)
    return [p.strip() for p in parts if p.strip()]


def build_graph(sentences: list[str]):
    # TF-IDF cosine similarity as edge weight
    vocab = defaultdict(int)
    for s in sentences:
        for w in re.findall(r'[A-Za-z]{3,}', s.lower()):
            vocab[w] += 1
    def tfidf_vec(s):
        counts = defaultdict(int)
        tokens = [w for w in re.findall(r'[A-Za-z]{3,}', s.lower())]
        for w in tokens:
            counts[w] += 1
        vec = {}
        for w, c in counts.items():
            idf = 1 + math.log((1 + len(sentences)) / (1 + vocab[w]))
            vec[w] = c * idf
        return vec
    vecs = [tfidf_vec(s) for s in sentences]
    def cosine(a, b):
        keys = set(a) | set(b)
        dot = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
        na = math.sqrt(sum(v*v for v in a.values()))
        nb = math.sqrt(sum(v*v for v in b.values()))
        return dot / (na * nb + 1e-9)
    n = len(sentences)
    graph = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                graph[i][j] = cosine(vecs[i], vecs[j])
    return graph


def textrank(graph, d=0.85, tol=1e-4, max_iter=200):
    n = len(graph)
    rank = [1.0/n]*n
    for _ in range(max_iter):
        prev = rank[:]
        for i in range(n):
            s = 0.0
            for j in range(n):
                if i != j:
                    out = sum(graph[j])
                    if out > 0:
                        s += graph[j][i] / out * prev[j]
            rank[i] = (1 - d) / n + d * s
        if sum(abs(rank[i]-prev[i]) for i in range(n)) < tol:
            break
    return rank


def summarize(text: str, max_sentences: int = 8) -> str:
    sents = sentence_split(text)
    if len(sents) <= max_sentences:
        return ' '.join(sents)
    graph = build_graph(sents)
    scores = textrank(graph)
    top_idx = sorted(range(len(sents)), key=lambda i: scores[i], reverse=True)[:max_sentences]
    top_idx.sort()
    return ' '.join(sents[i] for i in top_idx)
