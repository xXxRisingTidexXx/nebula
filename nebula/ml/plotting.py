from typing import Any, Dict, List
from pandas import DataFrame
from nebula.config import CONFIG
from nebula.snapshots import Snapshot
from plotly.graph_objects import Figure, Scattermapbox, Scatter3d
from plotly.subplots import make_subplots


def _show_flats(figure: Figure, flats: DataFrame):
    (
        figure
        .add_trace(Scatter3d(
            name='',
            x=flats['longitude'],
            y=flats['latitude'],
            z=flats['rate'],
            mode='markers',
            marker={'size': 4, 'color': flats['zone_id']},
            hovertemplate=(
                '<b>Координати</b>: (%{x:.3f}, %{y:.3f})<br>'
                '<b>Середня вартість</b>: %{z:.2f}<br>'
                '<b>ID кластера</b>: %{text}'
            ),
            text=flats['zone_id']
        ))
        .update_layout(
            scene={
                'xaxis_title': 'Довгота',
                'yaxis_title': 'Широта',
                'zaxis_title': 'Вартість 1 кв. м. (у $ США)'
            }
        )
    )


def _show_zones(figure: Figure, sites: DataFrame, zones: List[Dict[str, Any]]):
    (
        figure
        .add_trace(Scattermapbox(
            name='',
            mode='markers',
            lon=sites['longitude'],
            lat=sites['latitude'],
            marker={'size': 8, 'color': 'red'},
            hovertemplate=(
                '<b>Координати</b>: (%{lon:.3f}, %{lat:.3f})<br>'
                '<b>Середня вартість</b>: %{text}'
            ),
            text=[f'{r:.2f}' for r in sites['rate']]
        ))
        .update_layout(
            mapbox={
                'accesstoken': CONFIG['mapbox']['token'],
                'style': 'outdoors',
                'center': {'lon': 30.5241361, 'lat': 50.4500336},
                'zoom': 9.5,
                'layers': [
                    {
                        'type': 'fill',
                        'below': 'traces',
                        'color': 'royalblue',
                        'opacity': 0.5,
                        'source': z
                    }
                    for z in zones
                ]
            }
        )
    )


def show_figure(snapshot: Snapshot, title: str):
    figure = make_subplots(
        cols=2,
        column_widths=[0.45, 0.55],
        specs=[[{'type': 'scatter3d'}, {'type': 'scattermapbox'}]]
    )
    _show_flats(figure, snapshot.flats)
    _show_zones(figure, snapshot.sites, snapshot.zones)
    (
        figure
        .update_layout(
            title=title,
            showlegend=False,
            margin={'t': 60, 'r': 10, 'b': 10, 'l': 20}
        )
        .show()
    )
