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
from .space import CoastalArea

def fp(rp):
    return sorted(glob(f"data/processed/{rp}/*.gz"))

return_periods = ['rp0001', 'rp0002', 'rp0005', 'rp0010', 'rp0050', 'rp0100', 'rp0250', 'rp0500', 'rp1000']

depth_fps = dict([(rp, fp(rp)) for rp in return_periods]) # depth filepaths

def call_flood_level(model):
    return model.space.max_depth

def call_migration_count(model):
    return model.migration_count

class Population(mesa.Model):
    def __init__(
        self,
        population_gzip_file="data/population.tif.gz",
        sea_zip_file="data/sea2.zip",
        world_zip_file="data/clip2.zip", # slightly redundant as preprocessed tif already masked
        building_file = "data/fairbourne_buildings.geojson",
        depth_gzip_file = depth_fps['rp0001'][0] # the initial baseline value in 2010

    ):
        super().__init__()
        self.step_count = 0
        self.num_agents = 0
        self.space = CoastalArea(crs="epsg:4326")
        self.space.load_data(population_gzip_file, sea_zip_file, world_zip_file)
        self.space.load_flood_depth(depth_gzip_file,world_zip_file)
        self._load_building_from_file(building_file, crs=self.space.crs)
        self.space.read_rasters()
        self.schedule = mesa.time.RandomActivation(self)
        self._create_households()
        self.migration_count = 0        
        self.datacollector = mesa.DataCollector(
            model_reporters={"Max Flood Inundation": call_flood_level, "Migration Count": call_migration_count},
            agent_reporters={"Adaptation":"flood_preparedness"},
        )


    def _create_households(self):
        household_size = 3.5 # no. of people per household. taken from Tierolf paper
        for cell in self.space.population_layer:
            popu_round = math.ceil(cell.population/household_size) # divide person population by household size
            if popu_round > 0: # all non-zero raster cells
                for _ in range(popu_round):
                    self.num_agents += 1
                    random_home = self.space.get_random_home()
                    household = Household(
                        unique_id=uuid.uuid4().int,
                        model=self,
                    )
                    household.set_home(random_home)
                    self.schedule.add(household)
        del self.space.homes # remove homes list to free from memory after initialisation

    def _load_building_from_file(self, buildings_file: str, crs: str):
        
        buildings_df = gpd.read_file(buildings_file)
        buildings_df = buildings_df.set_crs(self.space.crs,allow_override=True).to_crs(crs) # NOTE: drop all headers but needed, so performance is improved
        buildings_df["centroid"] = list(zip(buildings_df.centroid.x, buildings_df.centroid.y)) # polygons are small
        buildings_df["area"] = np.floor(buildings_df.geometry.to_crs("EPSG:27700").area) # to m2 # polygons are small
        building_creator = mg.AgentCreator(Building, model=self)
        buildings = building_creator.from_GeoDataFrame(buildings_df)
        self.space.add_buildings(buildings)

    def generate_return_period(self) -> float:
        
        rp0001 = 1-1/2-1/5-1/10-1/50-1/100-1/250-1/500-1/1000 # make the rp0001 the default if none of the other return periods occur

        probabilities = [rp0001,1/2,1/5,1/10,1/50,1/100,1/250,1/500,1/1000]
        sampled_return_period = np.random.choice(a = return_periods,p = probabilities)

        return sampled_return_period


    def update_flood_depths(self, year, rp):
        self.space.remove_latest_layer() # clear previous layer
        self.space.load_flood_depth(depth_fps[rp][year],"data/clip2.zip") # load next filepath based on randomly generated rp and replace flood layer
        self.space.read_rasters()


    def step(self): #from 2010 to 2080

        # run a step
        self.datacollector.collect(self)
        self.schedule.step()

        # get next flood depth layer
        self.step_count +=1
        self.update_flood_depths(self.step_count,self.generate_return_period())