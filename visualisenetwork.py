from libpysal import weights, examples
from contextily import add_basemap
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import geopandas


distance_band = 50

buildings_wgs84 = geopandas.read_file("data/fairbourne_buildings.geojson") # this guy is in WGS84
buildings = buildings_wgs84.to_crs("EPSG:27700") # reprojected EPSG is for the UK. unit is in metres
coordinates = np.column_stack((buildings.centroid.x, buildings.centroid.y)) 
dist = weights.DistanceBand.from_array(coordinates, threshold=distance_band)

network_fps = {50:"data/networks/neighbours_50m.graphml",25:"data/networks/neighbours_25m.graphml",0:"data/networks/neighbours_0m.graphml"}

graph_0 = nx.read_graphml(network_fps[0])
graph_50 = nx.read_graphml(network_fps[50])
graph_25 = nx.read_graphml(network_fps[25])

positions = dict(zip(graph_50.nodes, coordinates))

f, ax = plt.subplots(1, 3, figsize=(15, 5))


nx.draw(graph_0, positions, ax=ax[0], node_size=0.1, node_color="b",arrowsize=0.1)
nx.draw(graph_25, positions, ax=ax[1], node_size=0.1, node_color="b",arrowsize=0.1)
nx.draw(graph_50, positions, ax=ax[2], node_size=0.1, node_color="b",arrowsize=0.1)
plt.show()