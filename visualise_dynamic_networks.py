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
dist_weights = weights.DistanceBand(coordinates, threshold=25)
original_graph = dist_weights.to_networkx()

# Assign positions to original graph nodes
positions = {node: coord for node, coord in zip(original_graph.nodes, coordinates)}

# Step 2: Load the start and end networks
network_fps = {
    "start": "data\export_networks\dynamic_neighbours_2010_test_2024-05-09_08-06-46.graphml",
    "end": "data\export_networks\dynamic_neighbours_2079_test_2024-05-09_08-17-48.graphml"
}
graph_start = nx.read_graphml(network_fps["start"])
graph_end = nx.read_graphml(network_fps["end"])

# Convert node IDs in start and end graphs from integers to strings
graph_start = nx.relabel.convert_node_labels_to_integers(graph_start, first_label=0, ordering="default", label_attribute=None)
graph_end = nx.relabel.convert_node_labels_to_integers(graph_end, first_label=0, ordering="default", label_attribute=None)

# Step 3: Assign positions to the nodes of the start and end networks
positions_start = {node: positions[node] for node in graph_start.nodes if node in positions}
positions_end = {node: positions[node] for node in graph_end.nodes if node in positions}

# Plotting
plt.figure(figsize=(10, 8))

# Plot original graph
nx.draw_networkx_nodes(original_graph, positions, node_color='g', label='Original', node_size=10)
nx.draw_networkx_edges(original_graph, positions, width=0.5, edge_color='lightgreen', alpha=0.5)

# Plot start and end networks
nx.draw_networkx_nodes(graph_start, positions_start, node_color='r', label='Start', node_size=10)
nx.draw_networkx_nodes(graph_end, positions_end, node_color='b', label='End', node_size=2)

nx.draw_networkx_edges(graph_start, positions_start, width=0.5, edge_color='red', alpha=0.5)
nx.draw_networkx_edges(graph_end, positions_end, width=0.5, edge_color='lightblue', alpha=0.5)

plt.legend(loc='upper right')  # Place legend in upper right corner
plt.axis('off')  # Turn off axis
plt.show()
