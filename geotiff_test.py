import uuid
import random
import geopandas as gpd
import mesa
from mesa_geo.geoagent import GeoAgent
from mesa_geo.geospace import GeoSpace
from mesa_geo.raster_layers import Cell, RasterLayer
from agent.building import Building


raster_layer = RasterLayer.from_file(
    f"/vsigzip/{population_gzip_file}",
    cell_cls=CoastalCell,
    attr_name="population",
)
raster_layer.crs = world_size.crs
raster_layer.total_bounds = world_size.total_bounds
self.add_layer(raster_layer)