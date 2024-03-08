import math
import uuid
import random

import mesa
import mesa_geo as mg
import numpy as np
from shapely.geometry import Point

from .space import CoastalArea



migration_cost = 10 # £1k

def call_sea_level(model):
    return model.sea_level

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

class HouseholdAgent(mg.GeoAgent):
    """A household agent with randomised income, savings, flood preparedness."""
    def __init__(self, unique_id, model, geometry, crs, img_coord):
        super().__init__(unique_id, model, geometry, crs)

        # Randomise income, consumption, and savings
        self.income = np.random.normal(30, 10) # £1k, post tax and consumption
        self.savings = np.random.normal(30, 10) # £1k
        self.flood_preparedness = np.random.normal(0, 0.5) # metres of flood barrier
        self.elevation = 0 # initial height above sea level in metres
        self.amenity = np.random.normal(100,50) # amenity value of the location in £1k

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
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,moore=True,include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def adapt(self):
        self.flood_preparedness += 0.5
        self.savings -= 10
        

class CoastalModel(mesa.Model):
    """A model with some number of agents."""
    def __init__(self, N=10):
        self.num_agents = N
        self.step_count = 0
        self.schedule = mesa.time.RandomActivation(self)
        self.sea_level = 0 # max sea level in year timestep. unit is metres
        self.running = True

        # Read landscape file
        coast = np.genfromtxt(f'maps/fictional/levels.txt') # 0 is water, 1-3 is land
        land = np.where(coast > 0)

        # Initiate mesa grid class
        self.grid = mesa.space.MultiGrid(np.shape(coast)[0], np.shape(coast)[1], False)

        # Create N household agents
        for i in range(self.num_agents):
            a = HouseholdAgent(i, self)
            self.schedule.add(a)

            # Add the agent to a random land cell (i.e. not in the sea)

            position = self.random.randrange(np.shape(land)[1]) # Pick a random valid position - this can result in overlapping agents

            x = land[0][position]
            y = land[1][position]
            self.grid.place_agent(a, (x,y))

            self.elevation = coast[x][y]

        self.datacollector = mesa.DataCollector(
            model_reporters={"Sea Level": call_sea_level},
            agent_reporters={"Adaptation":"flood_preparedness"},
        )

    def step(self): #from 2010 to 2080

        self.step_count +=1
        self.sea_level += self.step_count/100 + np.random.normal(0, 0.5)# m/year # includes a flood variation
        self.datacollector.collect(self)
        self.schedule.step()