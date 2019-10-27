from nebula.clustering import kmeans
from nebula.db.queries import select_flats
from nebula.extenders import extend_flats
from plotly.express import scatter_3d

LOCALITY = 'Київ'


if __name__ == '__main__':
    flats = kmeans(extend_flats(select_flats(LOCALITY)))
    plot = scatter_3d(flats, 'longitude', 'latitude', 'rate', 'cluster_id')
    plot.update_traces(marker={'size': 3})
    plot.show()
