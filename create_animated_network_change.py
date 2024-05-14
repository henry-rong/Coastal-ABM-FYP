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
original_graph = nx.read_graphml(r"U:\Coastal-ABM-FYP\data\networks\dynamic_neighbours_check.graphml")

# Assign positions to original graph nodes
positions = {node: coord for node, coord in zip(original_graph.nodes, coordinates)}

# Folder containing the graph files
folder_path = r"U:\\Coastal-ABM-FYP\data\\export_networks\\"

# Get a list of files in the folder
graph_files = sorted(os.listdir(folder_path))

# Iterate through consecutive pairs of files
for i in range(len(graph_files) - 1):
    
    network_fps = graph_files[i]

    # Step 2: Load the start and end networks
    
    current_graph = nx.read_graphml(folder_path + network_fps)

    # Step 3: Assign positions to the nodes of the start and end networks
    positions_current_graph = {node: positions[node] for node in current_graph.nodes if node in positions}

    # Plot start and end graphs with position data
    # plt.figure(figsize=(4, 8))
    # nx.draw(current_graph, pos=positions_current_graph, node_size=2, width=0.2, node_color='r',alpha=1)
    plt.figure(figsize=(10, 10))
    nx.draw(current_graph, pos=positions_current_graph, node_size=2, width=0.1, node_color='r',alpha=1)
    
    # barmouth
    plt.xlim(260250,261775)
    plt.ylim(315365,317209)  

    # # fairbourne
    # plt.xlim(261000,261650)
    # plt.ylim(312100,313800)  


    # Save the plot as a PNG frame
    frame_name = f"graph_frame_{i+2010}.png"
    plt.title("Barmouth " + str(i+2010))
    plt.savefig(os.path.join(folder_path, frame_name), dpi=200)
    plt.close()

    print(f"Saved frame: {frame_name}")

print("All frames saved successfully!")