from nebula.clustering import kmeans
from nebula.db.queries import (
    select_primary_housing_flats,
    select_secondary_housing_flats
)
from nebula.extenders import extend_flats
from nebula.plotting import show_figure

LOCALITY = 'Київ'

PRIMARY_HOUSING_FLATS_CLUSTER_NUMBER = 350

SECONDARY_HOUSING_FLATS_CLUSTER_NUMBER = 600

if __name__ == '__main__':
    show_figure(
        kmeans(
            extend_flats(select_primary_housing_flats(LOCALITY)),
            PRIMARY_HOUSING_FLATS_CLUSTER_NUMBER
        ),
        kmeans(
            extend_flats(select_secondary_housing_flats(LOCALITY)),
            SECONDARY_HOUSING_FLATS_CLUSTER_NUMBER
        )
    )
