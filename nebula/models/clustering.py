from typing import Tuple
from numpy import ndarray
from pandas import DataFrame
from sklearn.cluster import KMeans


def kmeans(
    frame: DataFrame,
    cluster_number: int
) -> Tuple[ndarray, ndarray]:
    model = KMeans(cluster_number, max_iter=400).fit(frame)
    return model.labels_, model.cluster_centers_
