from typing import Callable
from nebula.ml.clustering import kmeans
from nebula.db.queries import (
    select_primary_housing_flats,
    select_secondary_housing_flats
)
from nebula.ml.plotting import show_figure
from concurrent.futures.process import ProcessPoolExecutor

LOCALITY = 'Київ'


def visualize(select_flats: Callable, cluster_number: int, title: str):
    flats, cluster_centers = kmeans(select_flats(LOCALITY), cluster_number)
    show_figure(flats, title)


if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=4) as executor:
        for result in executor.map(
            visualize,
            [select_primary_housing_flats, select_secondary_housing_flats],
            [350, 600],
            [
                f'{LOCALITY}, ринок первинного житла',
                f'{LOCALITY}, ринок вторинного житла'
            ]
        ):
            print('Visualizing...')
