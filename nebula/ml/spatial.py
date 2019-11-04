from typing import Tuple, Union, List
from geovoronoi import voronoi_regions_from_coords
from shapely.geometry import Polygon, MultiPolygon
from numpy import ndarray


def geovoronoi(
    sites: ndarray,
    boundaries: Union[MultiPolygon, Polygon]
) -> Tuple[List[Union[MultiPolygon, Polygon]], List[List[int]]]:
    polygons, points, assignments = voronoi_regions_from_coords(sites, boundaries)
    return polygons, assignments
