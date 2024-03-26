import uuid

import geopandas as gpd
import mesa
from mesa_geo.geoagent import GeoAgent
from mesa_geo.geospace import GeoSpace
from mesa_geo.raster_layers import Cell, RasterLayer
import pyogrio
gpd.options.io_engine = "pyogrio"


class CoastalCell(Cell): # the population rasterfile
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
    def __init__(self, crs):
        super().__init__(crs=crs)

    def load_data(self, population_gzip_file, sea_zip_file, world_zip_file,building_file):
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
        self.building = gpd.GeoDataFrame.from_file(building_file)
        self.add_agents(GeoAgent(uuid.uuid4().int, None, self.sea, self.crs))

    @property
    def population_layer(self):
        return self.layers[0]