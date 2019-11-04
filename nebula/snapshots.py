from typing import Union, List
from statistics import mean
from numpy import ndarray
from pandas import DataFrame
from shapely.geometry import MultiPolygon, Polygon
from nebula.db.queries import select_flats
from nebula.ml.clustering import kmeans
from nebula.ml.spatial import geovoronoi


class Snapshot:
    def __init__(
        self,
        flats: DataFrame,
        labels: ndarray,
        centroids: ndarray,
        polygons: List[Union[MultiPolygon, Polygon]],
        assignments: List[List[int]]
    ):
        self.flats = flats.copy()
        self.flats['zone_id'] = self._get_zones_ids(labels, assignments)
        self.zones = self._make_zones(centroids, polygons, assignments)

    @staticmethod
    def _get_zones_ids(labels: ndarray, assignments: List[List[int]]):
        mappings = {i: a[0] for a in assignments for i in a}
        return [mappings[l] for l in labels]

    @staticmethod
    def _make_zones(
        centroids: ndarray,
        polygons: List[Union[MultiPolygon, Polygon]],
        assignments: List[List[int]]
    ) -> List['Zone']:
        rates = centroids[:, [0]]
        return [
            Zone(p, mean(rates[i, 0] for i in a))
            for p, a in zip(polygons, assignments)
        ]

    def __str__(self) -> str:
        return f'(\n{self.flats},\n{self.zones}\n)'

    def __repr__(self) -> str:
        return f'(\n{self.flats},\n{self.zones}\n)'


class Zone:
    def __init__(self, polygon: Union[MultiPolygon, Polygon], rate: float):
        self.polygons = self._split_polygon(polygon)
        self.rate = rate

    def _split_polygon(
        self,
        polygon: Union[MultiPolygon, Polygon]
    ) -> List[DataFrame]:
        if isinstance(polygon, Polygon):
            return [self._get_coordinates(polygon)]
        return [self._get_coordinates(p) for p in polygon]

    @staticmethod
    def _get_coordinates(polygon: Polygon) -> DataFrame:
        return DataFrame(
            polygon.exterior.coords,
            columns=['longitude', 'latitude']
        )

    def __str__(self) -> str:
        return f'(\n{self.polygons},\n{self.rate}\n)'

    def __repr__(self) -> str:
        return f'(\n{self.polygons},\n{self.rate}\n)'


def make_snapshot(
    locality: str,
    housing: str,
    cluster_number: int,
    boundaries: Union[MultiPolygon, Polygon]
) -> Snapshot:
    flats = select_flats(locality, housing)
    labels, centroids = kmeans(flats, cluster_number)
    polygons, assignments = geovoronoi(centroids[:, [1, 2]], boundaries)
    return Snapshot(flats, labels, centroids, polygons, assignments)
