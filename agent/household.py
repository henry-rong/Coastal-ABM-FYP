import math
import random
import uuid
import mesa
import mesa_geo as mg
import numpy as np
import pyproj
from shapely.geometry import Point
from agent.building import Building

migration_cost = 10 # £1k

def damage(level):
    if level < 0:
        return 0
    else:
        # return (1/3*math.log(math.exp(-9/5) + level*3)+3/5)*10 # cost of damage in £1k, assuming 100 sq m house
        return level*10

def expected_utility(income, savings, flood_preparedness, elevation, property_value, sea_level):
    """Calculate the expected utility of the household."""
    sums = savings + property_value + income

    flood_damage = damage(sea_level)

    # Adapt
    if sea_level < elevation:
        nothing = sums
    else:
        nothing = sums - flood_damage
    
    adapt = sums + damage(flood_preparedness) - flood_damage
    
    # Migrate
    migrate = sums - migration_cost

    utility = {nothing:'nothing', adapt:'adapt', migrate:'migrate'}

    # returns string of the action with the highest utility
    return utility.get(max(utility))

# class Household(mg.GeoAgent):
class Household(mesa.Agent):
    unique_id: int # household_id used to link households and building nodes
    model: mesa.Model
    # geometry: Point
    # crs: pyproj.CRS
    my_home: Building

    # MOBILITY_RANGE_X = 0.0
    # MOBILITY_RANGE_Y = 0.0

    # def __init__(self, unique_id, model, geometry, crs, img_coord):
    #     super().__init__(unique_id, model, geometry, crs)
    #     self.img_coord = img_coord

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        # Randomise income, consumption, and savings
        self.my_home = None
        self.income = np.random.normal(30, 10) # £1k, post tax and consumption
        self.savings = np.random.normal(30, 10) # £1k
        

    def set_home(self, new_home: Building ) -> None:
        new_home.occupied = 1
        self.my_home = new_home
        self.model.space.occupied.add(self.my_home.unique_id)


    def step(self):
        # dictionary of expected utility
        utility_case = expected_utility(self.income, self.savings, self.my_home.flood_preparedness, self.my_home.elevation, self.my_home.property_value, self.model.sea_level)
        match utility_case:
            case 'nothing':
                if self.model.sea_level > self.my_home.elevation + self.my_home.flood_preparedness: # flooded
                    self.my_home.property_value -= damage(self.model.sea_level)
                    
                pass
            case 'adapt':
                self.adapt()
            case 'migrate':
                self.migrate()

    def migrate(self) -> None:

        self.model.migration_count += 1
        self.my_home.occupied = 0
        
        new_home_id = random.choice(list(self.model.space.building_ids.difference(self.model.space.occupied))) # if slow, look at https://stackoverflow.com/questions/15993447/python-data-structure-for-efficient-add-remove-and-random-choice
        new_home = self.model.space._buildings.get(new_home_id)
        self.model.space.occupied.remove(self.my_home.unique_id)
        self.set_home(new_home)


    def adapt(self):
        self.my_home.flood_preparedness += 0.5
        self.savings -= 10