from typing import List
from pandas import DataFrame
from nebula.snapshots import Snapshot, Zone
from plotly.graph_objects import Figure, Scattermapbox, Scatter3d
from plotly.subplots import make_subplots


def _calc_color(rate: float) -> str:
    if rate < 400:
        return 'blue'
    if rate < 2000:
        return 'green'
    return 'red'


def _show_zones(figure: Figure, zones: List[Zone]):
    figure.add_trace(Scattermapbox(
        mode='markers',
        lon=[30.4],
        lat=[50.5],
        marker={'size': 10, 'color': ['cyan']}
    ))
    figure.update_layout(
        margin={'t': 60, 'r': 0, 'b': 10, 'l': 10},
        mapbox={
            'style': 'stamen-terrain',
            'center': {'lon': -73.605, 'lat': 45.51},
            'zoom': 12,
            'layers': [
                {
                    'type': 'fill',
                    'below': 'traces',
                    'color': 'royalblue',
                    'source': {
                        'type': 'FeatureCollection',
                        'features': [{
                            'type': 'Feature',
                            'geometry': {
                                'type': 'MultiPolygon',
                                'coordinates': [[[
                                    [-73.606352888, 45.507489991], [-73.606133883, 45.50687600],
                                    [-73.605905904, 45.506773980], [-73.603533905, 45.505698946],
                                    [-73.602475870, 45.506856969], [-73.600031904, 45.505696003],
                                    [-73.599379992, 45.505389066], [-73.599119902, 45.505632008],
                                    [-73.598896977, 45.505514039], [-73.598783894, 45.505617001],
                                    [-73.591308727, 45.516246185], [-73.591380782, 45.516280145],
                                    [-73.596778656, 45.518690062], [-73.602796770, 45.521348046],
                                    [-73.612239983, 45.525564037], [-73.612422919, 45.525642061],
                                    [-73.617229085, 45.527751983], [-73.617279234, 45.527774160],
                                    [-73.617304713, 45.527741334], [-73.617492052, 45.527498362],
                                    [-73.617533258, 45.527512253], [-73.618074188, 45.526759105],
                                    [-73.618271651, 45.526500673], [-73.618446320, 45.526287943],
                                    [-73.618968507, 45.525698560], [-73.619388002, 45.525216750],
                                    [-73.619532966, 45.525064183], [-73.619686662, 45.524889290],
                                    [-73.619787038, 45.524770086], [-73.619925742, 45.524584939],
                                    [-73.619954486, 45.524557690], [-73.620122362, 45.524377961],
                                    [-73.620201713, 45.524298907], [-73.620775593, 45.523650879]
                                ]]]
                            }
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
