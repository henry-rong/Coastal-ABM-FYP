import osmnx as ox
import geopandas as gpd
import pyogrio
gpd.options.io_engine = "pyogrio" # need to use this engine instead of fiona to avoid write error due to list

world_zip_file="data/clip2.zip"
world_size = gpd.GeoDataFrame.from_file(world_zip_file)

west, south, east, north = world_size.total_bounds

# fairbourne_buildings = ox.graph_from_bbox(box_bounds[3],box_bounds[1],box_bounds[0],box_bounds[2],network_type = 'all_private')
# ox.plot_graph(ox.project_graph(fairbourne_buildings))

tags = {'building': True, 'residential': ['urban','rural','detached','duplex','irregular_settlement','trailer_park','terrace','block']} 

# buildings = ox.features_from_bbox(box_bounds[3],box_bounds[1],box_bounds[0],box_bounds[2], tags)
buildings = ox.features_from_bbox(bbox=(north,south,east,west), tags=tags)
buildings.head()
buildings.plot(figsize = (100,100))

# buildings.to_file("./data/fairbourne_buildings.geojson",driver='GeoJSON')