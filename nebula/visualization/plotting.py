from typing import Any, Dict, List
from pandas import DataFrame
from nebula.config import CONFIG
from plotly.graph_objects import Figure, Scattermapbox, Scatter3d
from nebula.visualization.color_scales import ColorScale


def show_flats(flats: DataFrame, title: str):
    (
        Figure()
        .add_trace(Scatter3d(
            name='',
            x=flats['longitude'],
            y=flats['latitude'],
            z=flats['rate'],
            mode='markers',
            marker={
                'size': 4,
                'color': flats['zone_id'],
                'showscale': True,
                'colorbar': {'title': 'ID кластера'}
            },
            hovertemplate=(
                '<b>Координати</b>: (%{x:.3f}, %{y:.3f})<br>'
                '<b>Середня вартість</b>: %{z:.2f} $<br>'
                '<b>ID кластера</b>: %{text}'
            ),
            text=flats['zone_id']
        ))
        .update_layout(
            title=title,
            scene={
                'xaxis_title': 'Довгота',
                'yaxis_title': 'Широта',
                'zaxis_title': 'Вартість 1 кв. м., $'
            },
            showlegend=False
        )
        .show()
    )


def show_zones(sites: DataFrame, zones: List[Dict[str, Any]], title: str):
    color_scale = ColorScale(sites['rate'])
    (
        Figure()
        .add_trace(Scattermapbox(
            name='',
            mode='markers',
            lon=sites['longitude'],
            lat=sites['latitude'],
            marker={
                'size': 0,
                'showscale': True,
                'colorscale': color_scale.colors,
                'cmin': color_scale.min_tick,
                'cmax': color_scale.max_tick,
                'colorbar': {
                    'tick0': color_scale.min_tick,
                    'dtick': (color_scale.max_tick - color_scale.min_tick) / 6
                }
            },
            hovertemplate=(
                '<b>Координати</b>: (%{lon:.3f}, %{lat:.3f})<br>'
                '<b>Середня вартість</b>: %{text} $'
            ),
            text=[f'{r:.2f}' for r in sites['rate']]
        ))
        .update_layout(
            title=title,
            showlegend=False,
            mapbox={
                'accesstoken': CONFIG['mapbox']['token'],
                'style': 'outdoors',
                'center': {'lon': 30.5241361, 'lat': 50.4500336},
                'zoom': 9.5,
                'layers': [
                    {
                        'type': 'fill',
                        'below': 'traces',
                        'color': color_scale[r],
                        'opacity': 0.85,
                        'source': z
                    }
                    for r, z in zip(sites['rate'], zones)
                ]
            }
        )
        .show()
    )
