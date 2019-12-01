from typing import Tuple
from numpy import ndarray
from pandas import DataFrame
from sklearn.cluster import KMeans


def kmeans(frame: DataFrame, k: int) -> Tuple[ndarray, ndarray]:
    model = KMeans(k, max_iter=400).fit(frame)
    return model.labels_, model.cluster_centers_
