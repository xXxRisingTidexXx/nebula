from pandas import read_sql, DataFrame
from sqlalchemy import create_engine, select
from nebula.config import DSN
from nebula.db.tables import Geolocations, Flats


def select_flats(locality: str) -> DataFrame:
    with create_engine(DSN).connect() as connection:
        return read_sql(
            select([
                Flats.c.id,
                Flats.c.rate,
                Geolocations.c.point.ST_AsGeoJSON().label('point')
            ])
            .select_from(Flats.join(Geolocations))
            .where(Geolocations.c.locality == locality),
            connection,
            index_col=['id']
        )
