from concurrent.futures.process import ProcessPoolExecutor
from nebula.visualization.plotting import show_flats, show_zones
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
                [350, 550],
                [boundaries, boundaries]
            ),
            [
                f'{locality}, групування первинного житла '
                f'за територіальними та ціновими ознаками',
                f'{locality}, групування вторинного житла '
                f'за територіальними та ціновими ознаками'
            ]
        ):
            show_flats(snapshot.flats, title)
            show_zones(snapshot.sites, snapshot.zones, title)


if __name__ == '__main__':
    main()
