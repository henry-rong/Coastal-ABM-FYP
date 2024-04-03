import uuid
from random import randrange
import numpy as np
import mesa
import mesa_geo as mg
import pyproj
from shapely.geometry import Polygon

class Building(mg.GeoAgent):
    unique_id: int  # an ID that represents the building
    model: mesa.Model
    geometry: Polygon
    crs: pyproj.CRS
    centroid: mesa.space.FloatCoordinate
    name: str

    def __init__(self, unique_id, model, geometry, crs) -> None:
        super().__init__(unique_id=unique_id, model=model, geometry=geometry, crs=crs)
        self.name = str(uuid.uuid4())
        self.occupied = 0 # At initialisation, all homes are empty
        self.flood_preparedness = np.random.normal(0, 0.5) # metres of flood barrier
        # self.flood_preparedness = 69
        self.elevation = 0 # initial height above sea level in metres        
        self.property_value = np.random.normal(100,50) # amenity value of the location in £1k
        # self.amenity = 100

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(unique_id={self.unique_id}, name={self.name}",
            f"centroid={self.centroid})"
        )

    def __eq__(self, other):
        if isinstance(other, Building):
            return self.unique_id == other.unique_id
        return False