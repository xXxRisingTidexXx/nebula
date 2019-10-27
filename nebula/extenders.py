from pandas import DataFrame
from simplejson import loads


def extend_flats(flats: DataFrame) -> DataFrame:
    extended = flats.copy()
    extended['point'] = extended['point'].map(lambda p: loads(p)['coordinates'])
    extended['longitude'] = extended['point'].map(lambda p: p[0])
    extended['latitude'] = extended['point'].map(lambda p: p[1])
    return extended.drop(columns=['point'])
