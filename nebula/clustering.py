from pandas import DataFrame
from sklearn.cluster import KMeans


def kmeans(frame: DataFrame, cluster_number: int) -> DataFrame:
    clusterized = frame.copy()
    clusterized['cluster_id'] = (
        KMeans(cluster_number).fit_predict(clusterized.iloc[:, 0:4])
    )
    return clusterized
