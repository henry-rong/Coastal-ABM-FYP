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
from datetime import datetime

current_directory = os.getcwd() # for debugging
# os.chdir(current_directory)

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
        data_label, # for documentation of results
        # parameters
        neighbourhood_radius,
        initial_flood_experience,
        initial_flood_preparedness,
        house_sample_size,
        savings_mean,
        income_mean,
        fixed_migration_cost,
        variable_migration_cost,
        # geospatial data
        population_gzip_file="data/population.tif.gz",
        sea_zip_file="data/sea2.zip",
        world_zip_file="data/clip2.zip", # slightly redundant if preprocessed tif already masked
        building_file = "data/fairbourne_buildings.geojson"
    ):
        super().__init__()
        self.data_label = data_label
        # Counters
        self.step_count = 0
        self.num_agents = 0
        self.migration_count = 0  
        # NetworkX graphs
        self.neighbours_lookup = nx.convert_node_labels_to_integers(nx.read_graphml(network_fps[neighbourhood_radius]))
        self.dynamic_neighbours = copy.deepcopy(self.neighbours_lookup)
        # nx.write_graphml(self.dynamic_neighbours, f"data/export_networks/dynamic_neighbours_check.graphml")
        # Perception factors
        self.initial_flood_experience = initial_flood_experience
        self.house_sample_size = house_sample_size
        # Cost factors
        self.savings_mean = savings_mean
        self.income_mean = income_mean
        self.fixed_migration_cost = fixed_migration_cost
        self.variable_migration_cost = variable_migration_cost
        # Load space
        self.space = CoastalArea(crs="epsg:4326")
        self.space.load_data(population_gzip_file, sea_zip_file, world_zip_file)
        self.space.load_flood_depth(depth_fps[return_periods[initial_flood_preparedness]][0], world_zip_file)
        self._load_building_from_file(building_file, crs=self.space.crs)
        self.space.initial_rasters()
        self.schedule = mesa.time.RandomActivation(self)
        self._create_households()
              
        self.datacollector = mesa.DataCollector(
            model_reporters={"Max Flood Inundation": call_flood_level, "Migration Count": call_migration_count},
            agent_reporters={
                "Adaptation":"home_flood_preparedness",
             "Flood Damage":"flood_damage",
              "Floods experienced": "floods_experienced",
              "Nothing Utility":"nothing_utility",
              "Adapt Utility":"adapt_utility",
              "Migrate Utility":"migrate_utility",
              "Income":"income",
              "Savings":"savings"
              },)

    def _create_households(self):
        occupied_houses = set()
        OSM_households = 1154 # number of buildings extracted from OSM
        Census_households = 506 + 1341
        Census_fairbourne = 383 # households with usual residents
        Census_barmouth = 1146 # households with usual residents
        OSM_fairbourne = math.floor(Census_fairbourne*OSM_households/Census_households) # occupied proportion
        OSM_barmouth = math.floor(Census_barmouth*OSM_households/Census_households)
        OSM_single = math.floor(165/Census_fairbourne*OSM_fairbourne + 572/Census_barmouth*OSM_barmouth) # 'census_single_fairbourne'
        household_sizes = [1 for x in range(OSM_single)] + [3 for x in range(OSM_barmouth + OSM_fairbourne - OSM_single)] # individual and families
        age_means = [22,27,37,52,62,69,79,87,90] # mean of Census age bins
        age_ps = [0.0625,0.0625,0.1875,0.25,0.1125,0.1625,0.1125,0.025,0.025] # associated propabilities for both Fairbourne and Barmouth in 2011
        age_means_full = [2,6,8,12,15,16,18,22,27,37,52,62,69,79,87,90]
        age_ps_full = [0.06,0.03,0.02,0.04,0.01,0.02, 0.02,0.05,0.05,0.15,0.2,0.09,0.13,0.09,0.02,0.02]
        
        for _ in range(len(household_sizes)):
            self.num_agents += 1
            random_home = self.space.get_random_home()
            occupied_houses.add(random_home.unique_id)
            sampled_ages = []
            sampled_ages.append(np.random.choice(age_means,p=age_ps))
            if household_sizes[_] > 1:
                for people in range(1,household_sizes[_]):
                    sampled_ages.append(np.random.choice(age_means,p=age_ps))
                
            household = Household(
                unique_id=uuid.uuid4().int,
                model=self,
                household_size= household_sizes[_],
                ages = np.array(sampled_ages)
            )
            household.set_home(random_home)
            self.schedule.add(household)

        nodes_to_remove = self.space.building_ids.difference(occupied_houses) # get node ids of unoccupied houses
        self.dynamic_neighbours.remove_nodes_from(list(nodes_to_remove))
        del self.space.homes
        # nx.write_graphml(self.dynamic_neighbours, f"data/export_networks/dynamic_neighbours_initialised_check.graphml")

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

    def save_network_state(self, step):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nx.write_graphml(self.dynamic_neighbours, f"data/export_networks/dynamic_neighbours_{step+2010}_{self.data_label}_{timestamp}.graphml")

    def step(self):

        # if self.step_count == 0 or self.step_count == 69 or self.step_count == 68:
        self.save_network_state(self.step_count)
        print("the graph has " + str(self.dynamic_neighbours.number_of_edges()) + " edges and "+ str(self.dynamic_neighbours.number_of_nodes()) + " nodes!")

        self.datacollector.collect(self)
        self.schedule.step()
        self.step_count += 1
        self.update_flood_depths(self.step_count, self.generate_return_period())