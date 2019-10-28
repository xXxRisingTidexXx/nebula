from pandas import DataFrame
from plotly.subplots import make_subplots
from plotly.graph_objects import Scatter3d


def show_figure(
    primary_housing_flats: DataFrame,
    secondary_housing_flats: DataFrame
):
    figure = make_subplots(cols=2, specs=[[{'type': 'scene'}, {'type': 'scene'}]])
    figure.add_traces(Scatter3d(), row=1, col=1)
    figure.add_traces(Scatter3d(), row=1, col=2)
    figure.update_layout(width=1024, height=800, showlegend=False)
    figure.show()
