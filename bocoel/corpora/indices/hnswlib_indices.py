from __future__ import annotations

import numpy as np
from hnswlib import Index as _HnswlibIndex
from numpy.typing import NDArray

from bocoel.corpora.interfaces import Embedder, Index, Storage


class HnswlibIndex(Index):
    def __init__(self, key: str, embeddings: NDArray, threads: int = -1) -> None:
        if embeddings.ndim != 2:
            raise ValueError(f"Expected embeddings to be 2D, got {embeddings.ndim}D.")

        num_elems, dims = embeddings.shape

        self._key = key
        self._dims = dims
        self._ranges = np.stack([np.min(embeddings), np.max(embeddings)])

        self._index = _HnswlibIndex(max_elements=num_elems, threads=threads)
        self._index.add_items(embeddings)

    def key(self) -> str:
        return self._key

    def ranges(self) -> NDArray:
        return self._ranges

    def dims(self) -> int:
        return self._dims

    def search(self, query: NDArray, k: int = 1) -> NDArray:
        return self._index.knn_query(query, k=k)

    @classmethod
    def from_fields(cls, store: Storage, emb: Embedder, key: str) -> Index:
        items = [store[idx][key] for idx in range(len(store))]
        embedded = emb(items)
        return cls(key, embedded)