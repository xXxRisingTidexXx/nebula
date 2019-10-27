from pandas import DataFrame
from sklearn.cluster import KMeans

CLUSTER_NUMBER = 220

TOLERANCE = 1e-7


def kmeans(frame: DataFrame) -> DataFrame:
    clusterized = frame.copy()
    clusterized['cluster_id'] = (
        KMeans(CLUSTER_NUMBER, tol=TOLERANCE)
        .fit_predict(clusterized.iloc[:, 0:4])
    )
    return clusterized
