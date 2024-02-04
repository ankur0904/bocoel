import os
from collections.abc import Sequence

import torch
from torch import Tensor

from bocoel.corpora.embedders.interfaces import Embedder


class EnsembleEmbedder(Embedder):
    def __init__(self, embedders: Sequence[Embedder], sequential: bool = False) -> None:
        # Check if all embedders have the same batch size.
        self._embedders = embedders
        self._batch_size = embedders[0].batch
        if len(set(emb.batch for emb in embedders)) != 1:
            raise ValueError("All embedders must have the same batch size")

        self._sequential = sequential

        cpus = os.cpu_count()
        assert cpus is not None
        self._cpus = cpus

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({[str(emb) for emb in self._embedders]})"

    @property
    def batch(self) -> int:
        return self._batch_size

    @property
    def dims(self) -> int:
        return sum(emb.dims for emb in self._embedders)

    def _encode(self, texts: Sequence[str]) -> Tensor:
        results = [emb._encode(texts) for emb in self._embedders]
        return torch.cat([res.cpu() for res in results], dim=-1)
