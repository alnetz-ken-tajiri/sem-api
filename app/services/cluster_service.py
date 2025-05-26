from typing import List, Tuple
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, pairwise_distances

def auto_kmeans(
    embeddings: List[List[float]],
    k_min: int = 2,
    k_max: int = 10,
    metric: str = "cosine",
    tie_tol: float = 0.02,
) -> Tuple[int, List[int], float]:
    """
    Silhouette 最大化で最適 k を選択
    Returns (k_best, labels, best_score)
    """
    X = np.asarray(embeddings, dtype=np.float32)
    best_k, best_labels, best_sc = k_min, None, -1.0

    for k in range(k_min, min(k_max, len(X)) + 1):
        labels = KMeans(n_clusters=k, n_init="auto", random_state=42).fit_predict(X)
        # cosine のときは距離行列を使う
        if metric == "cosine":
            dist = pairwise_distances(X, metric="cosine")
            sc = silhouette_score(dist, labels, metric="precomputed")
        else:
            sc = silhouette_score(X, labels, metric=metric)

        if sc > best_sc + 1e-5 or (abs(sc - best_sc) <= tie_tol and k < best_k):
            best_k, best_labels, best_sc = k, labels, sc

    return best_k, best_labels.tolist(), best_sc
