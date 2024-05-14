import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from libpysal import weights

# Step 1: Create the original graph and assign positions
buildings_geojson = gpd.read_file("data/fairbourne_buildings.geojson")
buildings = buildings_geojson.to_crs("EPSG:27700")
coordinates = np.column_stack((buildings.centroid.x, buildings.centroid.y))
dist_weights = weights.DistanceBand(coordinates, threshold=50)
# original_graph = dist_weights.to_networkx()
original_graph = nx.read_graphml(r"U:\Coastal-ABM-FYP\data\networks\dynamic_neighbours_check.graphml") # original graph but with str nodes

# Assign positions to original graph nodes
positions = {node: coord for node, coord in zip(original_graph.nodes, coordinates)}

# Step 2: Load the start and end networks
# network_fps = {
#     "start": "data\export_networks\dynamic_neighbours_check.graphml",
#     "end": "data\export_networks\dynamic_neighbours_initialised_check.graphml"
# }
network_fps = {
    "start": "data\export_networks\dynamic_neighbours_2010_test_2024-05-09_08-06-46.graphml",
    "end": "data\export_networks\dynamic_neighbours_2079_test_2024-05-09_08-17-48.graphml"
}
graph_start = nx.read_graphml(network_fps["start"])
graph_end = nx.read_graphml(network_fps["end"])

# Step 3: Assign positions to the nodes of the start and end networks
positions_start = {node: positions[node] for node in graph_start.nodes if node in positions}
positions_end = {node: positions[node] for node in graph_end.nodes if node in positions}

# Plotting
# plt.figure(figsize=(10, 10))
plt.figure(figsize=(12, 32))

linewidth = 0.1
nodesize = 3

# Plot original graph
nx.draw_networkx_nodes(original_graph, positions, node_color='g', label='Unoccupied', node_size=nodesize)
nx.draw_networkx_edges(original_graph, positions, width=linewidth, edge_color='green', alpha=1)

# Plot start and end networks
nx.draw_networkx_nodes(graph_start, positions_start, node_color='r', label='2010', node_size=nodesize)
nx.draw_networkx_nodes(graph_end, positions_end, node_color='b', label='2080', node_size=nodesize)

nx.draw_networkx_edges(graph_start, positions_start, width=linewidth, edge_color='red', alpha=1)
nx.draw_networkx_edges(graph_end, positions_end, width=linewidth, edge_color='blue', alpha=1)

plt.legend(loc='upper right')  # Place legend in upper right corner
plt.axis('off')  # Turn off axis

# # barmouth
# plt.xlim(260250,261775)
# plt.ylim(315365,317209)  

# fairbourne
plt.xlim(261000,261650)
plt.ylim(312100,313800)  

plt.show()
