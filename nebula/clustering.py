from typing import Tuple
from pandas import DataFrame
from sklearn.cluster import KMeans


def kmeans(frame: DataFrame, cluster_number: int) -> Tuple[DataFrame, DataFrame]:
    new_frame = frame.copy()
    model = KMeans(cluster_number).fit(new_frame.iloc[:, 0:4])
    new_frame['cluster_id'] = model.labels_
    return (
        new_frame,
        DataFrame(
            model.cluster_centers_,
            columns=['rate', 'longitude', 'latitude']
        )
    )
