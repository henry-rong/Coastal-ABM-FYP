import math
import random
import uuid
import mesa
import mesa_geo as mg
import numpy as np
from shapely.geometry import Point

migration_cost = 10 # £1k

def damage(level):
    if level < 0:
        return 0
    else:
        # return (1/3*math.log(math.exp(-9/5) + level*3)+3/5)*10 # cost of damage in £1k, assuming 100 sq m house
        return level*10

def expected_utility(income, savings, flood_preparedness, elevation, amenity, sea_level):
    """Calculate the expected utility of the household."""
    sums = savings + amenity + income

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

class Household(mg.GeoAgent):

    MOBILITY_RANGE_X = 0.0
    MOBILITY_RANGE_Y = 0.0

    def __init__(self, unique_id, model, geometry, crs, img_coord):
        super().__init__(unique_id, model, geometry, crs)
        self.img_coord = img_coord

        # Randomise income, consumption, and savings
        self.income = np.random.normal(30, 10) # £1k, post tax and consumption
        self.savings = np.random.normal(30, 10) # £1k
        self.flood_preparedness = np.random.normal(0, 0.5) # metres of flood barrier
        self.elevation = 0 # initial height above sea level in metres
        self.amenity = np.random.normal(100,50) # amenity value of the location in £1k
        

    def set_random_world_coord(self):
        world_coord_point = Point(self.model.space.population_layer.transform * self.img_coord)
        random_world_coord_x = world_coord_point.x + np.random.uniform(-self.MOBILITY_RANGE_X, self.MOBILITY_RANGE_X)
        random_world_coord_y = world_coord_point.y + np.random.uniform(-self.MOBILITY_RANGE_Y, self.MOBILITY_RANGE_Y)
        self.geometry = Point(random_world_coord_x, random_world_coord_y)

    def step(self):
        # dictionary of expected utility
        utility_case = expected_utility(self.income, self.savings, self.flood_preparedness, self.elevation, self.amenity, self.model.sea_level)

        match utility_case:
            case 'nothing':
                if self.model.sea_level > self.elevation + self.flood_preparedness: # flooded
                    self.amenity -= damage(self.model.sea_level) 
                pass
            case 'adapt':
                self.adapt()
            case 'migrate':
                self.migrate()

    def migrate(self):

        self.model.migration_count += 1
        neighborhood = self.model.space.population_layer.get_neighborhood(self.img_coord, moore=True)
        found = False
        while neighborhood and not found:
            next_img_coord = random.choice(neighborhood)
            world_coord_point = Point(self.model.space.population_layer.transform * next_img_coord)
            if world_coord_point.within(self.model.space.sea):
                neighborhood.remove(next_img_coord)
                continue
            else:
                found = True
                self.img_coord = next_img_coord
                self.set_random_world_coord()

    def adapt(self):
        self.flood_preparedness += 0.5
        self.savings -= 10