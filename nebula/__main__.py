from argparse import ArgumentParser
from nebula.utils import check_namespace
from nebula.visualization.plotting import show_flats, show_zones
from nebula.nominatim import get_boundaries
from nebula.snapshots import make_snapshot


if __name__ == '__main__':
    parser = ArgumentParser(
        prog='nebula',
        description='Ukrainian realty analysis CLI'
    )
    parser.add_argument(
        '--locality',
        help='target locality; for instance, \'Київ\'',
        default='Київ'
    )
    parser.add_argument(
        '--housing',
        help='housing type — primary/secondary',
        default='primary'
    )
    parser.add_argument('--k', help='number of clusters', default=100)
    locality, housing, k = check_namespace(parser.parse_args())
    snapshot = make_snapshot(locality, housing, k, get_boundaries(locality))
    title = f'{locality}, {housing} housing'
    show_flats(snapshot.flats, title)
    show_zones(snapshot.sites, snapshot.zones, title)
