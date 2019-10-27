from trafaret import Dict, String, Int

config_trafaret = Dict(
    database=Dict(
        user=String,
        password=String,
        host=String,
        port=Int,
        database=String
    )
)
