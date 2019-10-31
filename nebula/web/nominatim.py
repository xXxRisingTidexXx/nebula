from typing import Any, Dict
from pandas import DataFrame
from requests import get


geocoding_url = (
    'https://nominatim.openstreetmap.org/search?q={}'
    '&polygon=1&limit=1&polygon_geojson=1&format=json'
)


def _geocode(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    response = get(geocoding_url.format(*args, **kwargs), timeout=5)
    if not (200 <= response.status_code < 300):
        raise RuntimeError('Nominatim geocoding request failed')
    json = response.json()
    if len(json) == 0:
        raise RuntimeError('Nominatim has no responses to your query')
    return json[0]


def get_boundaries(locality: str) -> DataFrame:
    return DataFrame(_geocode(locality)['polygonpoints'])
