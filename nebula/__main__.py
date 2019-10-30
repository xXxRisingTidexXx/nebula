from typing import Callable
from nebula.clustering import kmeans
from nebula.db.queries import (
    select_primary_housing_flats,
    select_secondary_housing_flats
)
from nebula.extenders import extend_flats
from nebula.plotting import show_figure
from concurrent.futures.process import ProcessPoolExecutor
from nebula.spatial import voronoi

LOCALITY = 'Київ'


def visualize(select_flats: Callable, cluster_number: int, title: str):
    flats, cluster_centers = kmeans(
        extend_flats(select_flats(LOCALITY)),
        cluster_number
    )
    show_figure(flats, title)
    voronoi(cluster_centers)


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
