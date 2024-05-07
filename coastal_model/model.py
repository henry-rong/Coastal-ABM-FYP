import os
import math
import random
import uuid
from glob import glob
import mesa
import mesa_geo as mg
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from agent.household import Household
from agent.building import Building
from .space import CoastalArea  # Assuming space.py is in the same directory
import networkx as nx
import copy

def fp(rp):
    return sorted(glob(os.path.join("data", "processed", rp, "*.gz")))

return_periods = ['rp0001', 'rp0002', 'rp0005', 'rp0010', 'rp0050', 'rp0100', 'rp0250', 'rp0500', 'rp1000']

depth_fps = {rp: fp(rp) for rp in return_periods}  # depth filepaths

network_fps = {50: "data/networks/neighbours_50m.graphml",
               25: "data/networks/neighbours_25m.graphml",
               0: "data/networks/neighbours_0m.graphml"}

def call_flood_level(model):
    return model.space.max_depth

def call_migration_count(model):
    return model.migration_count

class CoastalModel(mesa.Model):
    def __init__(
        self,
        people_per_household,
        neighbourhood_radius,
        initial_flood_experience,
        initial_flood_preparedness,
        house_sample_size,
        fixed_migration_cost,
        household_adaptation_cost,
        population_gzip_file="data/population.tif.gz",
        sea_zip_file="data/sea2.zip",
        world_zip_file="data/clip2.zip", # slightly redundant if preprocessed tif already masked
        building_file = "data/fairbourne_buildings.geojson"
    ):
        super().__init__()
        self.neighbours_lookup = nx.convert_node_labels_to_integers(nx.read_graphml(network_fps[neighbourhood_radius]))
        self.dynamic_neighbours = copy.deepcopy(self.neighbours_lookup)
        self.step_count = 0
        self.num_agents = 0
        self.people_per_household = people_per_household
        self.initial_flood_experience = initial_flood_experience
        self.house_sample_size = house_sample_size
        self.fixed_migration_cost = fixed_migration_cost
        self.household_adaptation_cost = household_adaptation_cost
        self.space = CoastalArea(crs="epsg:4326")
        self.space.load_data(population_gzip_file, sea_zip_file, world_zip_file)
        self.space.load_flood_depth(depth_fps[return_periods[initial_flood_preparedness]][0], world_zip_file)
        self._load_building_from_file(building_file, crs=self.space.crs)
        self.space.initial_rasters()
        self.schedule = mesa.time.RandomActivation(self)
        self._create_households()
        self.migration_count = 0        
        self.datacollector = mesa.DataCollector(
            model_reporters={"Max Flood Inundation": call_flood_level, "Migration Count": call_migration_count},
            agent_reporters={
                "Adaptation":"home_flood_preparedness",
             "Flood Damage":"flood_damage",
              "Floods experienced": "floods_experienced",
              "Nothing Utility":"nothing_utility",
              "Adapt Utility":"adapt_utility",
              "Migrate Utility":"migrate_utility",
              "Savings":"savings"
              },)

    def _create_households(self):
        occupied_houses = set()
        household_size = self.people_per_household
        for cell in self.space.population_layer:
            popu_round = math.ceil(cell.population/household_size)
            if popu_round > 0:
                for _ in range(popu_round):
                    self.num_agents += 1
                    random_home = self.space.get_random_home()
                    occupied_houses.add(random_home.unique_id)
                    household = Household(
                        unique_id=uuid.uuid4().int,
                        model=self,
                    )
                    household.set_home(random_home)
                    self.schedule.add(household)

        nodes_to_remove = self.space.building_ids.difference(occupied_houses)
        self.dynamic_neighbours.remove_nodes_from(list(nodes_to_remove))
        del self.space.homes

    def _load_building_from_file(self, buildings_file: str, crs: str):
        buildings_df = gpd.read_file(buildings_file)
        buildings_df = buildings_df.set_crs(self.space.crs, allow_override=True).to_crs(crs)
        buildings_df["centroid"] = list(zip(buildings_df.centroid.x, buildings_df.centroid.y))
        buildings_df["area"] = np.floor(buildings_df.geometry.to_crs("EPSG:27700").area)
        buildings_df["length"] = np.floor(buildings_df.geometry.to_crs("EPSG:27700").length)
        building_creator = mg.AgentCreator(Building, model=self)
        buildings = building_creator.from_GeoDataFrame(buildings_df)
        self.space.add_buildings(buildings)

    def generate_return_period(self) -> float:
        rp0001 = 1-1/2-1/5-1/10-1/50-1/100-1/250-1/500-1/1000
        probabilities = [rp0001,1/2,1/5,1/10,1/50,1/100,1/250,1/500,1/1000]
        sampled_return_period = np.random.choice(a=return_periods, p=probabilities)
        return sampled_return_period

    def update_flood_depths(self, year, rp):
        self.space.remove_latest_layer()
        self.space.load_flood_depth(depth_fps[rp][year], "data/clip2.zip")
        self.space.read_rasters()

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.step_count += 1
        self.update_flood_depths(self.step_count, self.generate_return_period())