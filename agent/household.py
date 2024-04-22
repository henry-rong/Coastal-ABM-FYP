import math
import random
import uuid
import mesa
import mesa_geo as mg
import numpy as np
import pyproj
from shapely.geometry import Point
from agent.building import Building

migration_cost = 10 # £1k - needs to change to scale with property value

def damage(level, area):
    if level < 0:
        return 0
    
    elif (level < 5.363): #
        cost_per_m2 =  -0.0338*level**2 + 0.3626*level
        # need to do pound to euro conversion with time - state as limitation
        return cost_per_m2 * area
    else:
        return area
    
def defence_cost():
    return 10


class Household(mesa.Agent):
    unique_id: int # household_id used to link households and building nodes
    model: mesa.Model
    my_home: Building


    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        # Randomise income, consumption, and savings
        self.my_home = None
        self.income = np.random.normal(30, 10) # £1k, post tax and consumption
        self.savings = np.random.normal(30, 10) # £1k
        self.floods_experienced = 0 # dependent on timesteps since last flood....
        self.timesteps_since_last_flood = 0 # parameter to randomly initialise
        

    def set_home(self, new_home: Building ) -> None:
        new_home.occupied = 1
        self.my_home = new_home
        self.model.space.occupied.add(self.my_home.unique_id)

    def expected_utility(self, income, savings, flood_preparedness, property_value, flood_level, damage):

        """Calculate the expected utility of the household."""
        sums = savings + property_value + income

        flood_damage = damage

        # Nothing
        if flood_level < flood_preparedness:
            nothing = sums
        else: # flooded!
            nothing = sums - flood_damage
        
        # Adapt - assuming perfect defence
        adapt = sums - defence_cost()
        
        # Migrate
        migrate = sums - migration_cost

        utility = {nothing:'nothing', adapt:'adapt', migrate:'migrate'}

        # returns string of the action with the highest utility
        return utility.get(max(utility))

    def step(self):
        
        step_damage = damage(self.my_home.inundation,self.my_home.area) # calculate once

        

        # return outcome of expected utility
        utility_case = self.expected_utility(
            income = self.income, 
            savings= self.savings, 
            flood_preparedness=self.my_home.flood_preparedness, 
            property_value=self.my_home.property_value, 
            flood_level=self.my_home.inundation,
            damage=step_damage)
        
        match utility_case:
            case 'nothing':
                # apply damage
                if self.my_home.flood_preparedness : # flooded
                    self.my_home.property_value -= step_damage
                pass
            case 'adapt':
                self.adapt()
            case 'migrate':
                self.migrate()

    def sample_properties(self, num_properties):

        # return property value of new home to migration cost first before comitting - need to inspect attributes of flood prepardness, property value, area / household size ratio

        properties = {}

        for property in range(num_properties):

            new_home_id = random.choice(list(self.model.space.building_ids.difference(self.model.space.occupied))) # if slow, look at https://stackoverflow.com/questions/15993447/python-data-structure-for-efficient-add-remove-and-random-choice
            new_home = self.model.space._buildings.get(new_home_id)

            properties["new_home_id"] = new_home

        return properties

    def evaluate_properties(properties: dict):

        # calculates fixed cost and variable migration costs

        for property_id, property in properties:
            ...

        # return property_cost

    def migrate(self, new_home) -> None:

        # update migration count, replaces old home with new one, and returns old home to pool of unoccupied homes

        self.model.migration_count += 1
        self.my_home.occupied = 0

        self.model.space.occupied.remove(self.my_home.unique_id)
        self.set_home(new_home)

        # drop old node from network
        G = self.model.dynamic_neighbours

        G.remove_node(str(self.my_home.unique_id))

        # update network
        new_node = str(new_home.unique_id)
        edges_to_copy = self.model.neighbours_lookup.edges(new_node)

        for edge in edges_to_copy:
            # Add the edge only if both endpoints exist in the graph
            if G.has_node(edge[0]) and G.has_node(edge[1]):
                if edge[0] == 2:
                    G.add_edge(new_node, edge[1])
                else:
                    G.add_edge(edge[0], new_node)


    def adapt(self) -> None:
        self.my_home.flood_preparedness += 0.5
        self.savings -= 10