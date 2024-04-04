import math
import random
import uuid
import mesa
import mesa_geo as mg
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from agent.household import Household
from agent.building import Building
from .space import CoastalArea

# define functions

def call_sea_level(model):
    return model.sea_level

def call_migration_count(model):
    return model.migration_count

class Population(mesa.Model):
    def __init__(
        self,
        population_gzip_file="data/population.tif.gz",
        sea_zip_file="data/sea2.zip",
        world_zip_file="data/clip2.zip",
        building_file = "data/fairbourne_buildings.geojson"

    ):
        super().__init__()
        self.step_count = 0
        self.num_agents = 0
        self.space = CoastalArea(crs="epsg:4326")
        self.space.load_data(population_gzip_file, sea_zip_file, world_zip_file)
        self._load_building_from_file(building_file, crs=self.space.crs)
        pixel_size_x, pixel_size_y = self.space.population_layer.resolution
        # Household.MOBILITY_RANGE_X = pixel_size_x / 2
        # Household.MOBILITY_RANGE_Y = pixel_size_y / 2
        self.schedule = mesa.time.RandomActivation(self)
        self._create_households()
        self.migration_count = 0
        
        # sea level rise

        self.sea_level = 0 # max sea level in year timestep. unit is metres
        self.datacollector = mesa.DataCollector(
            model_reporters={"Sea Level": call_sea_level, "Migration Count": call_migration_count},
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
                        # crs=self.space.crs,
                        # img_coord=cell.indices,
                    )
                    household.set_home(random_home)
                    # self.space.add_agents(household) # not needed as Household agent is no longer geoagent
                    self.schedule.add(household)
        del self.space.homes # remove homes list to free from memory after initialisation

    def _load_building_from_file(self, buildings_file: str, crs: str):
        
        buildings_df = gpd.read_file(buildings_file)
        buildings_df = buildings_df.set_crs(self.space.crs,allow_override=True).to_crs(crs)
        buildings_df["centroid"] = list(zip(buildings_df.centroid.x, buildings_df.centroid.y)) # polygons are small
        building_creator = mg.AgentCreator(Building, model=self)
        buildings = building_creator.from_GeoDataFrame(buildings_df)
        self.space.add_buildings(buildings)


    def step(self): #from 2010 to 2080

        self.step_count +=1
        stochastic_storm = np.random.choice(a = [0, 2 + self.step_count],p = [(1 - (1+self.step_count/100)/100),(1+self.step_count/100)/100])
        self.sea_level += self.step_count/1000 + stochastic_storm # m/year # includes a flood variation
        self.datacollector.collect(self)
        self.schedule.step()
        self.sea_level -= stochastic_storm

        