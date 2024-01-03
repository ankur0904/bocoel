from typing import Any

import numpy as np
from numpy import linalg
from numpy.typing import NDArray
from typing_extensions import Self

from bocoel.corpora.indices import utils
from bocoel.corpora.interfaces import Distance, Index, InternalSearchResult


class WhiteningIndex(Index):
    """
    Whitening index. Whitens the data before indexing.
    See https://arxiv.org/abs/2103.15316 for more info.
    """

    def __init__(
        self,
        embeddings: NDArray,
        remains: int,
        distance: str | Distance,
        backend: type[Index],
        **kwargs: Any
    ) -> None:
        # Remains might be smaller than embeddings.
        # In such case, no dimensionality reduction is performed.
        remains = min(remains, embeddings.shape[1])

        white = self.whiten(embeddings, remains)
        assert white.shape[1] == remains, {
            "whitened": white.shape,
            "remains": remains,
        }
        self._index = backend.from_embeddings(
            embeddings=white, distance=distance, **kwargs
        )
        assert remains == self._index.dims

    @property
    def embeddings(self) -> NDArray:
        return self._index.embeddings

    @property
    def distance(self) -> Distance:
        return self._index.distance

    @property
    def dims(self) -> int:
        return self._index.dims

    @property
    def bounds(self) -> NDArray:
        return self._index.bounds

    def _search(self, query: NDArray, k: int = 1) -> InternalSearchResult:
        return self._index._search(query, k=k)

    @classmethod
    def from_embeddings(
        cls, embeddings: NDArray, distance: str | Distance, **kwargs: Any
    ) -> Self:
        return cls(embeddings=embeddings, distance=distance, **kwargs)

    @staticmethod
    def whiten(embeddings: NDArray, k: int) -> NDArray:
        embeddings = utils.normalize(embeddings)

        mean = embeddings.mean(axis=0, keepdims=True)
        covar = np.cov(embeddings.T)

        u, v, _ = linalg.svd(covar)
        sqrt_inv_v = 1 / (v**0.5)
        w = u @ np.diag(sqrt_inv_v)[:, :k]

        white = (embeddings - mean) @ w
        return white
