from concurrent.futures.process import ProcessPoolExecutor
from nebula.visualization.plotting import show_figure
from nebula.web.nominatim import get_boundaries
from nebula.snapshots import make_snapshot


def main():
    locality = 'Київ'
    boundaries = get_boundaries(locality)
    with ProcessPoolExecutor(max_workers=2) as executor:
        for snapshot, title in zip(
            executor.map(
                make_snapshot,
                [locality, locality],
                ['primary', 'secondary'],
                [300, 900],
                [boundaries, boundaries]
            ),
            [
                f'{locality}, групування первинного житла за '
                f'розміщенням та вартістю 1 кв. м. житлової площі',
                f'{locality}, групування вторинного житла за '
                f'розміщенням та вартістю 1 кв. м. житлової площі'
            ]
        ):
            show_figure(snapshot, title)


if __name__ == '__main__':
    main()
