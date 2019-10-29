from pandas import DataFrame
from plotly.express import scatter_3d


def show_figure(flats: DataFrame, title: str):
    figure = scatter_3d(
        flats,
        'longitude',
        'latitude',
        'rate',
        'cluster_id',
        title=title
    )
    figure.update_traces(marker={'size': 3, 'opacity': 0.8})
    figure.show()
