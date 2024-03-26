import math
import random
import uuid
import mesa
import mesa_geo as mg
import numpy as np
from shapely.geometry import Point
from agent.household import Household
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
        self.space = CoastalArea(crs="epsg:4326")
        self.space.load_data(population_gzip_file, sea_zip_file, world_zip_file, building_file)
        pixel_size_x, pixel_size_y = self.space.population_layer.resolution
        Household.MOBILITY_RANGE_X = pixel_size_x / 2
        Household.MOBILITY_RANGE_Y = pixel_size_y / 2
        self.schedule = mesa.time.RandomActivation(self)
        self._create_agents()
        self.migration_count = 0

        # sea level rise

        self.sea_level = 0 # max sea level in year timestep. unit is metres
        self.datacollector = mesa.DataCollector(
            model_reporters={"Sea Level": call_sea_level, "Migration Count": call_migration_count},
            agent_reporters={"Adaptation":"flood_preparedness"},
        )

    def _create_agents(self):
        household_size = 3.5 # no. of people per household. taken from Tierolf paper
        num_agents = 0
        for cell in self.space.population_layer:
            popu_round = math.ceil(cell.population/household_size)
            if popu_round > 0: # all non-zero raster cells
                for _ in range(popu_round):
                    num_agents += 1
                    point = Point(self.space.population_layer.transform * cell.indices)
                    if not point.within(self.space.sea): # that are not in the sea
                        household = Household(
                            unique_id=uuid.uuid4().int,
                            model=self,
                            crs=self.space.crs,
                            geometry=point,
                            img_coord=cell.indices,
                        )
                        household.set_random_world_coord()
                        self.space.add_agents(household)
                        self.schedule.add(household)

    def step(self): #from 2010 to 2080

        self.step_count +=1
        stochastic_storm = np.random.choice(a = [0, 2 + self.step_count],p = [(1 - (1+self.step_count/100)/100),(1+self.step_count/100)/100])
        self.sea_level += self.step_count/1000 + stochastic_storm # m/year # includes a flood variation
        self.datacollector.collect(self)
        self.schedule.step()
        self.sea_level -= stochastic_storm