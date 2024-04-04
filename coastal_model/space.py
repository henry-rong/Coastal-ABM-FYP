import uuid
import random
import geopandas as gpd
import mesa
from mesa_geo.geoagent import GeoAgent
from mesa_geo.geospace import GeoSpace
from mesa_geo.raster_layers import Cell, RasterLayer
from agent.building import Building

from typing import Dict, Tuple, DefaultDict

import pyogrio
gpd.options.io_engine = "pyogrio"

class CoastalCell(Cell): # this class is used to represent each cell in the raster layer
    population: float | None

    def __init__(
        self,
        pos: mesa.space.Coordinate | None = None,
        indices: mesa.space.Coordinate | None = None,
    ):
        super().__init__(pos, indices)
        self.population = None

    def step(self):
        pass


class Sea(GeoAgent):
    pass


class CoastalArea(GeoSpace):
    #type hints
    homes: Tuple[Building]
    home_counter: DefaultDict[mesa.space.FloatCoordinate, int]
    _buildings: Dict[int, Building]


    def __init__(self, crs):
        super().__init__(crs=crs)
        self.homes = [] # a list of homes for initialisation
        self._buildings = {} # a dictionary containing key: unique_id value: Building
        self.building_ids = set() # a set of all building unique_id
        self.occupied = set() # a set of occupied building_id

    def load_data(self, population_gzip_file, sea_zip_file, world_zip_file):
        world_size = gpd.GeoDataFrame.from_file(world_zip_file)
        
        raster_layer = RasterLayer.from_file(
            f"/vsigzip/{population_gzip_file}",
            cell_cls=CoastalCell,
            attr_name="population",
        )
        raster_layer.crs = world_size.crs
        raster_layer.total_bounds = world_size.total_bounds
        self.add_layer(raster_layer)

        self.sea = gpd.GeoDataFrame.from_file(sea_zip_file).geometry[0]
        
        self.add_agents(GeoAgent(uuid.uuid4().int, None, self.sea, self.crs))

    @property
    def population_layer(self):
        return self.layers[0]
    
    # Add all Buildings from OSM data to the space 
    def add_buildings(self, agents) -> None: # note that agent here refers to the Building agent, not the Household agent
        super().add_agents(agents)
        for agent in agents:
            if isinstance(agent, Building):
                self._buildings[agent.unique_id] = agent # a buildings dictionary with unique_id keys
                self.homes.append(agent) # append a Building agent
                self.building_ids.add(agent.unique_id)

   
    def update_home_counter(  # is this needed?
            self,
            home_pos: mesa.space.FloatCoordinate
    ) -> None:
        self.home_counter[home_pos] += 1

    def get_random_home(self) -> Building:
        random_building = random.choice(self.homes)
        self.homes.remove(random_building) 
        return random_building