from typing import List
from pandas import DataFrame
from nebula.snapshots import Snapshot, Zone
from plotly.graph_objects import layout, Figure, Scatter, Scatter3d


def _calc_color(rate: float) -> str:
    if rate < 400:
        return 'blue'
    if rate < 2000:
        return 'green'
    return 'red'


def _show_zones(figure: Figure, zones: List[Zone], title: str):
    # zones_figure = Figure()
    for zone in zones:
        for polygon in zone.polygons:
            figure.add_trace(Scatter(
                x=polygon['longitude'],
                y=polygon['latitude'],
                fill='toself',
                fillcolor=_calc_color(zone.rate),
                hoveron='points+fills',
                text=f'Rate: {zone.rate}',
                line_width=1,
                line_color='black'
            ))
    # figure.add_trace(zones_figure)


def _show_flats(figure: Figure, flats: DataFrame, title: str):
    figure.add_trace(Scatter3d(
        x=flats['longitude'],
        y=flats['latitude'],
        z=flats['rate'],
        mode='markers',
        marker={
            'size': 3,
            'color': flats['zone_id']
        }
    ))


def show_figure(
    snapshot: Snapshot,
    figure_title: str,
    zones_title: str,
    flats_title: str
):
    figure = Figure()
    _show_zones(figure, snapshot.zones, zones_title)
    # _show_flats(figure, snapshot.flats, flats_title)
    (
        figure.update_layout(
            width=650,
            height=650,
            title=figure_title,
            showlegend=False,
            margin={'t': 70, 'r': 10, 'b': 10, 'l': 10}
        )
        .update_xaxes(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            showline=True,
            linewidth=2,
            linecolor='gray',
            mirror=True
        )
        .update_yaxes(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            showline=True,
            linewidth=2,
            linecolor='gray',
            mirror=True
        )
        .show()
    )
