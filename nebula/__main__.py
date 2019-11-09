from typing import List, Union
from shapely.geometry import MultiPolygon, Polygon
from concurrent.futures.process import ProcessPoolExecutor
from nebula.visualization.plotting import show_figure
from nebula.web.nominatim import get_boundaries
from nebula.snapshots import make_snapshot, Snapshot


def make_snapshots(
    locality: str,
    boundaries: Union[Polygon, MultiPolygon]
) -> List[Snapshot]:
    with ProcessPoolExecutor(max_workers=2) as executor:
        return list(executor.map(
            make_snapshot,
            [locality, locality],
            ['primary', 'secondary'],
            [300, 600],
            [boundaries, boundaries]
        ))


def main():
    locality = 'Київ'
    show_figure(
        make_snapshot(
            locality,
            'secondary',
            900,
            get_boundaries(locality)
        ),
        f'{locality}, групування вторинного житла за '
        f'розміщенням та вартістю 1 кв. м. житлової площі'
    )


if __name__ == '__main__':
    main()
