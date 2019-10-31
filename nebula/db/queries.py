from pandas import read_sql, DataFrame
from simplejson import loads
from sqlalchemy import create_engine, select, and_
from sqlalchemy.sql import ClauseElement, Selectable
from nebula.config import DSN
from nebula.db.tables import Geolocations, Flats, FlatsDetails, Details


def _select_flats(clause: ClauseElement) -> DataFrame:
    with create_engine(DSN).connect() as connection:
        flats = read_sql(
            select([
                Flats.c.id,
                Flats.c.rate,
                Geolocations.c.point.ST_AsGeoJSON().label('point')
            ])
            .select_from(Flats.join(Geolocations))
            .where(clause),
            connection,
            index_col=['id']
        )
        flats['point'] = flats['point'].map(lambda p: loads(p)['coordinates'])
        flats['longitude'] = flats['point'].map(lambda p: p[0])
        flats['latitude'] = flats['point'].map(lambda p: p[1])
        return flats.drop(columns=['point'])


def _query_primary_housing_flats() -> Selectable:
    return (
        select([FlatsDetails.c.flat_id])
        .select_from(FlatsDetails.join(Details))
        .where(Details.c.value.in_(
            ['Первинне житло', 'На етапі будівництва']
        ))
    )


def select_primary_housing_flats(locality: str) -> DataFrame:
    return _select_flats(and_(
        Geolocations.c.locality == locality,
        Flats.c.id.in_(_query_primary_housing_flats())
    ))


def select_secondary_housing_flats(locality: str) -> DataFrame:
    return _select_flats(and_(
        Geolocations.c.locality == locality,
        Flats.c.id.notin_(_query_primary_housing_flats())
    ))
