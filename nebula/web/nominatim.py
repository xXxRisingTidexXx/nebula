from typing import Any, Dict, List, Union
from requests import get
from shapely.geometry import shape, Polygon, MultiPolygon
from nebula.utils import find

_geocoding_url = (
    'https://nominatim.openstreetmap.org/search?q={}&polygon_geojson=1&format=json'
)


def _geocode(locality: str) -> List[Dict[str, Any]]:
    response = get(_geocoding_url.format(locality), timeout=5)
    if not (200 <= response.status_code < 300):
        raise RuntimeError('Nominatim geocoding request failed')
    return response.json()


def get_boundaries(locality: str) -> Union[Polygon, MultiPolygon]:
    placement = find(
        lambda p: p['geojson']['type'] in {'Polygon', 'MultiPolygon'},
        _geocode(locality)
    )
    if not placement:
        raise RuntimeError('Nominatim didn’t find any placement')
    return shape(placement['geojson']).buffer(0)
