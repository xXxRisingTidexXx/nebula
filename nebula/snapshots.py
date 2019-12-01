from typing import Union, List, Any, Dict
from numpy import ndarray, mean
from pandas import DataFrame
from shapely.geometry import MultiPolygon, Polygon, mapping
from nebula.db.queries import select_flats
from nebula.models.clustering import kmeans
from nebula.models.spatial import geovoronoi


def make_snapshot(
    locality: str,
    housing: str,
    k: int,
    boundaries: Union[MultiPolygon, Polygon]
) -> 'Snapshot':
    flats = select_flats(locality, housing)
    labels, centroids = kmeans(flats, k)
    polygons, assignments = geovoronoi(centroids[:, [1, 2]], boundaries)
    return Snapshot(flats, labels, centroids, polygons, assignments)


class Snapshot:
    def __init__(
        self,
        flats: DataFrame,
        labels: ndarray,
        centroids: ndarray,
        polygons: List[Union[MultiPolygon, Polygon]],
        assignments: List[List[int]]
    ):
        self.flats = self._make_flats(flats, labels, assignments)
        self.sites = self._make_sites(centroids, assignments)
        self.zones = self._make_zones(polygons)

    @staticmethod
    def _make_flats(
        flats: DataFrame,
        labels: ndarray,
        assignments: List[List[int]]
    ) -> DataFrame:
        new_flats = flats.copy()
        mappings = {i: a[0] for a in assignments for i in a}
        new_flats['zone_id'] = [mappings[l] for l in labels]
        return new_flats

    @staticmethod
    def _make_sites(
        centroids: ndarray,
        assignments: List[List[int]]
    ) -> DataFrame:
        return DataFrame(
            [
                [
                    mean(centroids[a, 0]),
                    centroids[a[0], 1],
                    centroids[a[0], 2]
                ]
                for a in assignments
            ],
            columns=['rate', 'longitude', 'latitude']
        )

    @staticmethod
    def _make_zones(
        polygons: List[Union[MultiPolygon, Polygon]]
    ) -> List[Dict[str, Any]]:
        return [
            {
                'type': 'FeatureCollection',
                'features': [{
                    'type': 'Feature',
                    'geometry': mapping(p)
                }]
            }
            for p in polygons
        ]

    def __str__(self) -> str:
        return f'(\n{self.flats},\n{self.sites},\n{self.zones}\n)'

    def __repr__(self) -> str:
        return f'(\n{self.flats},\n{self.sites},\n{self.zones}\n)'
