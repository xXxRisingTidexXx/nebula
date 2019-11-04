from pandas import read_sql, DataFrame
from simplejson import loads
from sqlalchemy import create_engine, select, and_
from sqlalchemy.sql import Selectable
from nebula.config import DSN
from nebula.db.tables import Geolocations, Flats, FlatsDetails, Details


def _select(query: Selectable) -> DataFrame:
    with create_engine(DSN).connect() as connection:
        return read_sql(query, connection, index_col=['id'])


def _query_primary_housing_flats() -> Selectable:
    return (
        select([FlatsDetails.c.flat_id])
        .select_from(FlatsDetails.join(Details))
        .where(Details.c.value.in_(
            ['Первинне житло', 'На етапі будівництва']
        ))
    )


clauses = {
    'primary': lambda: Flats.c.id.in_(_query_primary_housing_flats()),
    'secondary': lambda: Flats.c.id.notin_(_query_primary_housing_flats())
}


def select_flats(locality: str, housing: str) -> DataFrame:
    flats = _select(
        select([
            Flats.c.id,
            Flats.c.rate,
            Geolocations.c.point.ST_AsGeoJSON().label('point')
        ])
        .select_from(Flats.join(Geolocations))
        .where(and_(Geolocations.c.locality == locality, clauses[housing]()))
    )
    coordinates = flats['point'].map(lambda p: loads(p)['coordinates'])
    flats['longitude'] = coordinates.map(lambda p: p[0])
    flats['latitude'] = coordinates.map(lambda p: p[1])
    return flats.drop(columns=['point'])
