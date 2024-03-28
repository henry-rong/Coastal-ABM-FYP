import math
import random
import uuid
import mesa
import mesa_geo as mg
import numpy as np
import geopandas as gpd

buildings_file = "data/fairbourne_buildings.geojson"

buildings_df = gpd.read_file(buildings_file)

# load_building_from_file(building_file, crs="epsg:4326")

# def load_building_from_file(buildings_file: str, crs: str):
    
#     # buildings_df = gpd.GeoDataFrame.from_file(buildings_file)
#     buildings_df = gpd.read_file(buildings_file)
#     buildings_df.drop("Id", axis=1, inplace=True)
#     buildings_df.index.name = "unique_id"
#     # buildings_df = buildings_df.set_crs(self.space.crs, allow_override=True).to_crs(crs)
#     # buildings_df = buildings_df.to_crs('+proj=cea').centroid.to_crs(buildings_df.crs)
#     buildings_df = buildings_df.set_crs(self.space.crs,allow_override=True).to_crs(crs)
#     buildings_df["centroid"] = list(zip(buildings_df.centroid.x, buildings_df.centroid.y))
#     building_creator = mg.AgentCreator(Building, model=self)
#     buildings = building_creator.from_GeoDataFrame(buildings_df)