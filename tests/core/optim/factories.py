from bocoel import AxServiceOptimizer, Corpus, KMeansOptimizer, Optimizer, Score


def ax_optim(corpus: Corpus, score: Score) -> Optimizer:
    steps = [
        {"model": "sobol", "num_trials": 5},
        {"model": "modular", "num_trials": -1},
    ]
    return AxServiceOptimizer.evaluate_corpus(corpus=corpus, score=score, steps=steps)


def kmeans_optim(corpus: Corpus, score: Score) -> Optimizer:
    return KMeansOptimizer.evaluate_corpus(corpus=corpus, score=score, n_clusters=3)
