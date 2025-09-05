from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
import math
from .bm25 import BM25Okapi

@dataclass
class Chunk:
    id: str
    text: str
    source: str
    meta: Dict[str, Any]

def cosine(a: List[float], b: List[float]) -> float:
    num = sum(x*y for x,y in zip(a,b))
    da = math.sqrt(sum(x*x for x in a)) or 1e-9
    db = math.sqrt(sum(y*y for y in b)) or 1e-9
    return num / (da * db)

class Embedder:
    """Interface for dense embeddings. In tests we patch/mock this."""
    def embed(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError

class HybridRetriever:
    """TODO: Implement true hybrid retrieval.
    Current baseline returns BM25 ranking only.
    You must:
      - compute BM25 scores
      - obtain embeddings for [query] + chunks via an injected Embedder
      - normalize both scores, then combine by alpha
      - deduplicate by source and return top-k
    """
    def __init__(self, chunks: List[Chunk], embedder: Optional[Embedder] = None):
        self.chunks = chunks
        self.embedder = embedder
        self._bm25 = BM25Okapi([c.text for c in chunks])

    def retrieve(self, query: str, k: int = 5, alpha: float = 0.5) -> List[Tuple[Chunk, float]]:
        # BASELINE: BM25 only (this will fail tests that expect hybrid improvements).
        bm25_scores = self._bm25.get_scores(query)
        scored = list(zip(self.chunks, bm25_scores))
        scored.sort(key=lambda x: x[1], reverse=True)
        # Dedup by source
        seen = set()
        out = []
        for ch, sc in scored:
            if ch.source in seen:
                continue
            seen.add(ch.source)
            out.append((ch, float(sc)))
            if len(out) >= k:
                break
        return out
