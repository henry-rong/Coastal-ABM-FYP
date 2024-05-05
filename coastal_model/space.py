import uuid
import random
import geopandas as gpd
import mesa
import math
import numpy as np
from mesa_geo.geoagent import GeoAgent
from mesa_geo.geospace import GeoSpace
from mesa_geo.raster_layers import Cell, RasterLayer
from agent.building import Building
from typing import Dict, Tuple, DefaultDict
import pyogrio

gpd.options.io_engine = "pyogrio"

class CoastalCell(Cell):
    population: float | None
    depth: float | None

    def __init__(
        self,
        pos: mesa.space.Coordinate | None = None,
        indices: mesa.space.Coordinate | None = None,
    ):
        super().__init__(pos, indices)
        self.population = None
        self.depth = None 

    def step(self):
        pass

class Sea(GeoAgent):
    pass

class CoastalArea(GeoSpace):
    homes: Tuple[Building]
    home_counter: DefaultDict[mesa.space.FloatCoordinate, int]
    _buildings: Dict[int, Building]

    def __init__(self, crs):
        super().__init__(crs=crs)
        self.homes = []
        self._buildings = {}
        self.building_ids = set()
        self.occupied = set()
        self.max_depth = None

    def load_data(self, population_gzip_file, sea_zip_file, world_zip_file) -> None:
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

    def add_buildings(self, agents) -> None:
        super().add_agents(agents)
        for agent in agents:
            if isinstance(agent, Building):
                self._buildings[agent.unique_id] = agent
                self.homes.append(agent)
                self.building_ids.add(agent.unique_id)

    def update_home_counter(
            self,
            home_pos: mesa.space.FloatCoordinate
    ) -> None:
        self.home_counter[home_pos] += 1

    def get_random_home(self) -> Building:
        random_building = random.choice(self.homes)
        self.homes.remove(random_building) 
        return random_building

    def load_flood_depth(self, depth_gzip_file, world_zip_file) -> None:
        world_size = gpd.GeoDataFrame.from_file(world_zip_file)
        raster_layer = RasterLayer.from_file(
            f"/vsigzip/{depth_gzip_file}",
            cell_cls=CoastalCell,
            attr_name="depth",
        )
        raster_layer.crs = world_size.crs
        raster_layer.total_bounds = world_size.total_bounds
        self.add_layer(raster_layer)

    @property
    def depth_layer(self):
        return self.layers[1]

    def read_rasters(self) -> None:
        raster_values = self.depth_layer.get_raster('depth')
        self.max_depth = np.amax(raster_values)
        max_depth_pos = np.unravel_index(np.argmax(raster_values),raster_values.shape)
        max_coord = self.cell_pos_to_coord(self.depth_layer,max_depth_pos[1:])
        for k,v in self._buildings.items():
            index = self.coord_to_cell_pos(self.depth_layer,self._buildings[k].centroid)
            depth_at_point = raster_values[0][index]
            self._buildings[k].inundation = depth_at_point

    def remove_latest_layer(self) -> None:
        self._static_layers.pop()

    def coord_to_cell_pos(self, layer, coordinates: Tuple) -> Tuple:
        x,y = coordinates
        min_x, min_y, max_x, max_y = layer.total_bounds
        return (math.floor((y - min_y)/(max_y-min_y)*(layer.height-1)),math.floor((x - min_x)/(max_x-min_x)*(layer.width-1)))

    def cell_pos_to_coord(self, layer, pos) -> Tuple:
        pos_y, pos_x = pos
        min_x, min_y, max_x, max_y = layer.total_bounds
        return (pos_x/(layer.width-1)*(max_x-min_x)+min_x,pos_y/(layer.height-1)*(max_y-min_y)+min_y)
