import os
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from libpysal import weights

# create original graph with all edges

buildings_geojson = gpd.read_file("data/fairbourne_buildings.geojson")
buildings = buildings_geojson.to_crs("EPSG:27700")
coordinates = np.column_stack((buildings.centroid.x, buildings.centroid.y))
dist_weights = weights.DistanceBand(coordinates, threshold=25)
original_graph = dist_weights.to_networkx()


# Folder containing the graph files
folder_path = r"U:\\Coastal-ABM-FYP\data\\export_networks\\"

# Get a list of files in the folder
graph_files = sorted(os.listdir(folder_path))

# Iterate through consecutive pairs of files
for i in range(len(graph_files) - 1):
    
    network_fps = graph_files[i]

    # Assign positions to original graph nodes
    positions = {node: coord for node, coord in zip(original_graph.nodes, coordinates)}

    # Step 2: Load the start and end networks
    
    current_graph = nx.read_graphml(folder_path + network_fps)

    # Convert node IDs in start and end graphs from integers to strings
    current_graph = nx.relabel.convert_node_labels_to_integers(current_graph, first_label=0, ordering="default", label_attribute=None)

    # Step 3: Assign positions to the nodes of the start and end networks
    positions_current_graph = {node: positions[node] for node in current_graph.nodes if node in positions}

    # Plot start and end graphs with position data
    plt.figure(figsize=(10, 8))
    nx.draw(current_graph, pos=positions_current_graph, with_labels=True, node_size=10, node_color='r')

    # Save the plot as a PNG frame
    frame_name = f"graph_frame_{i}.png"
    plt.savefig(os.path.join(folder_path, frame_name))
    plt.close()

    print(f"Saved frame: {frame_name}")

print("All frames saved successfully!")