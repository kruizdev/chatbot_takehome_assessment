import json
from app.retrieval.retriever import Chunk, HybridRetriever, Embedder
from app.retrieval.bm25 import BM25Okapi
from math import log2

def ndcg_at_k(ranked_ids, relevant_ids, k=5):
    dcg = 0.0
    for i, cid in enumerate(ranked_ids[:k], start=1):
        if cid in relevant_ids:
            dcg += 1.0 / (log2(i+1))
    # ideal
    ideal = 0.0
    for i in range(1, min(k, len(relevant_ids)) + 1):
        ideal += 1.0 / (log2(i+1))
    return dcg / ideal if ideal > 0 else 0.0

class DeterministicEmbedder(Embedder):
    def embed(self, texts):
        # cheap deterministic embed: map to vector of length 8 via char codes
        vecs = []
        for t in texts:
            v = [0.0]*8
            for i, ch in enumerate(t.lower()[:64]):
                v[i%8] += (ord(ch)%13)/13.0
            vecs.append(v)
        return vecs

def test_hybrid_beats_bm25_tmpset(tmp_path):
    # Load small corpus from airline jsonl
    path = (tmp_path / "airline_policies.jsonl")
    # Use the repo data file
    import pathlib
    repo_file = pathlib.Path("data/airline_policies.jsonl")
    with open(repo_file, "r", encoding="utf-8") as rf, open(path, "w", encoding="utf-8") as wf:
        wf.write(rf.read())

    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            chunks.append(Chunk(id=rec["id"], text=rec["summary"], source=rec.get("url") or rec["id"], meta={}))

    # load qas
    qas = []
    with open("tests/fixtures/qas.jsonl","r",encoding="utf-8") as f:
        for line in f:
            qas.append(json.loads(line))

    # Baseline BM25 ranking ndcg
    bm25 = BM25Okapi([c.text for c in chunks])
    def bm25_rank(q):
        sc = bm25.get_scores(q)
        ranked = [c.id for _, c in sorted(zip(sc, chunks), key=lambda x: x[0], reverse=True)]
        return ranked

    bm_ndcg = sum(ndcg_at_k(bm25_rank(q['q']), q['relevant_ids']) for q in qas) / len(qas)

    # Hybrid retriever (currently BM25-only in code) — must be implemented by candidate to improve
    hr = HybridRetriever(chunks, embedder=DeterministicEmbedder())
    def hybrid_rank(q):
        pairs = hr.retrieve(q, k=5, alpha=0.5)
        return [c.id for c,_ in pairs]

    hy_ndcg = sum(ndcg_at_k(hybrid_rank(q['q']), q['relevant_ids']) for q in qas) / len(qas)

    assert hy_ndcg >= bm_ndcg + 0.05, f"Expected hybrid to beat BM25 by 0.05; bm25={bm_ndcg:.3f}, hybrid={hy_ndcg:.3f}"
