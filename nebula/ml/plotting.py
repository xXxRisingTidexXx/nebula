from typing import List
from pandas import DataFrame
from nebula.snapshots import Snapshot
from plotly.graph_objects import Figure, Scattermapbox, Scatter3d
from plotly.subplots import make_subplots


def _show_zones(figure: Figure):
    figure.add_trace(Scattermapbox(
        mode='markers',
        lon=[30.4],
        lat=[50.5],
        marker={'size': 10, 'color': ['cyan']}
    ))
    figure.update_layout(
        margin={'t': 60, 'r': 0, 'b': 10, 'l': 10},
        mapbox={
            'style': 'open-street-map',
            'center': {'lon': 30.4, 'lat': 50.5},
            'zoom': 11,
            'layers': [
                {
                    'type': 'fill',
                    'below': 'traces',
                    'color': 'royalblue',
                    'source': {
                        'type': 'FeatureCollection',
                        'features': [{
                            'type': 'Feature',
                            'geometry': {}
                        }]
                    }
                }
            ]
        }
    )


def _show_flats(figure: Figure, flats: DataFrame):
    figure.add_trace(Scatter3d(
        x=flats['longitude'],
        y=flats['latitude'],
        z=flats['rate'],
        mode='markers',
        marker={'size': 3, 'color': flats['zone_id']}
    ))


def show_figure(snapshot: Snapshot, figure_title: str):
    figure = make_subplots(
        cols=2,
        column_widths=[0.55, 0.45],
        specs=[[{'type': 'scattermapbox'}, {'type': 'scatter3d'}]]
    )
    _show_zones(figure, snapshot.zones)
    _show_flats(figure, snapshot.flats)
    figure.update_layout(title=figure_title).show()
