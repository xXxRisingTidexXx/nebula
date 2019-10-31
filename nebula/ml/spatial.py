from pandas import DataFrame
from scipy.spatial import Voronoi


def voronoi(frame: DataFrame):
    v = Voronoi(frame.iloc[:, 1:3])
    print(v.vertices)
