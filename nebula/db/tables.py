from geoalchemy2 import Geometry
from sqlalchemy import (
    MetaData, Table, Column, Integer, String, Date, DECIMAL,
    Float, SmallInteger, ForeignKey, UniqueConstraint
)
from sqlalchemy_utils import URLType

metadata = MetaData()

Flats = Table(
    'flats',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('url', URLType(length=400), unique=True, nullable=False),
    Column('avatar', URLType(length=400)),
    Column('published', Date, nullable=False),
    Column('price', DECIMAL(10, 2), nullable=False),
    Column('rate', DECIMAL(10, 2), nullable=False),
    Column('area', Float, nullable=False),
    Column('living_area', Float),
    Column('kitchen_area', Float),
    Column('rooms', SmallInteger, nullable=False),
    Column('floor', SmallInteger, nullable=False),
    Column('total_floor', SmallInteger, nullable=False),
    Column('ceiling_height', Float),
    Column(
        'geolocation_id',
        Integer,
        ForeignKey('geolocations.id', ondelete='CASCADE'),
        nullable=False
    ),
    UniqueConstraint('rooms', 'floor', 'total_floor', 'geolocation_id')
)

Geolocations = Table(
    'geolocations',
    metadata,
    Column('id', Integer, primary_key=True),
    Column(
        'point',
        Geometry(geometry_type='POINT', srid=4326),
        unique=True,
        nullable=False
    ),
    Column('state', String(30)),
    Column('locality', String(40)),
    Column('county', String(40)),
    Column('neighbourhood', String(90)),
    Column('road', String(80)),
    Column('house_number', String(20))
)

Details = Table(
    'details',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('value', String(60), unique=True, nullable=False)
)

FlatsDetails = Table(
    'flats_details',
    metadata,
    Column('id', Integer, primary_key=True),
    Column(
        'flat_id',
        Integer,
        ForeignKey('flats.id', ondelete='CASCADE'),
        nullable=False
    ),
    Column(
        'detail_id',
        Integer,
        ForeignKey('details.id', ondelete='CASCADE'),
        nullable=False
    ),
    UniqueConstraint('flat_id', 'detail_id')
)
