import math
import random
import uuid
import mesa
import mesa_geo as mg
import numpy as np
import pyproj
from shapely.geometry import Point
from agent.building import Building
import geopandas as gpd


def death_function(input_age):
    
    if input_age < 87:
        life_p = 1
    elif input_age > 100:
        life_p = 0 # no centenarians sorry
    else:
        
        life_p = 0.00265277*input_age**2 -  0.543874*input_age + 27.8909 # polynomial
    np.random.choice([1,0],p=[1-life_p,life_p]) # death = 1, life = 0



def depth_damage_calculation(level, area):

    euro_to_pound = 0.86

    if level < 0:
        return 0
    
    elif (level < 5.363): #
        cost_per_m2 =  -0.0338*level**2 + 0.3626*level
        # need to do pound to euro conversion with time - state as limitation
        return cost_per_m2 * area *euro_to_pound # in k£
    else:
        return area # in k£
    

class Household(mesa.Agent):
    unique_id: int # household_id used to link households and building nodes
    model: mesa.Model
    my_home: Building


    def __init__(self, unique_id, model, household_size,ages):
        super().__init__(unique_id, model)

        # Randomise income, consumption, and savings
        self.household_size = household_size
        self.ages = np.array(ages)
        self.my_home = None
        self.savings =  np.count_nonzero(np.logical_and(ages > 18, ages < 66))*np.random.normal(self.model.savings_mean, 10) # £1k. multiply with all ages between graduation and retirement
        self.income = np.count_nonzero(np.logical_and(ages > 18, ages < 66))*np.random.normal(self.model.income_mean, 10) # £1k, disposable. multiply with all ages between graduation and retirement
        self.floods_experienced = self.model.initial_flood_experience # dependent on timesteps since last flood....
        self.timesteps_since_last_flood = 0 # parameter to randomly initialise
        self.home_flood_preparedness = 0
        self.flood_damage = 0
        self.nothing_utility = 0
        self.adapt_utility = 0
        self.migrate_utility= 0
        

    def set_home(self, new_home: Building ) -> None:
        new_home.occupied = 1
        self.my_home = new_home
        self.my_home.household_id = self.unique_id # assign household unique_id to building (so you can lookup household from Building)
        self.home_flood_preparedness = self.my_home.flood_preparedness
        self.model.space.occupied.add(self.my_home.unique_id)

    def expected_utility(self, savings, flood_preparedness, property_value, flood_level, damage, neighbourhood_attributes, destination, migration_cost):

        """Calculate the expected utility of the household."""
        sums = savings + property_value
        property_flood_damage = damage
        # [flood prepardness, property value, inundation height, floods experienced, time since last flood]
        
        n_flood_prep = neighbourhood_attributes[0]
        n_property_value = neighbourhood_attributes[1]
        n_inundation_height = neighbourhood_attributes[2]
        n_floods_experienced = neighbourhood_attributes[3]
        n_time_since_last_flood = neighbourhood_attributes[4]

        # Nothing
        if flood_level < flood_preparedness:
            nothing = sums
        else: # flooded!
            nothing = sums - property_flood_damage
        
        self.nothing_utility = nothing

        discounting_factor = max(n_floods_experienced,self.floods_experienced,1)/max(1,min(n_time_since_last_flood,self.timesteps_since_last_flood))

        # discounting_factor = 1

        # Adapt - assuming very cautious households
        peer_adaptation_level = max(n_inundation_height, n_flood_prep) # looking at neighbours, considering the max
        personal_adaptation_level = max(flood_level,n_inundation_height)
        max_flood_level = max(peer_adaptation_level,personal_adaptation_level)
        
        adapt = discounting_factor*(sums - self.defence_cost(max_flood_level)[0] + property_flood_damage)
        self.adapt_utility = adapt

        # Migrate
        migrate = discounting_factor*(sums - migration_cost - destination.property_value + depth_damage_calculation(destination.inundation,destination.area))
        self.migrate_utility = migrate

        utility = {nothing:'nothing', adapt:'adapt', migrate:'migrate'}

        """
        returns list containing:
        1. string of the action with the highest utility
        2. perceived flood adaptation level required
        """
        return [utility.get(max(utility)), max_flood_level]

    def step(self):
        
        # apply actions
        self.ages += 1 # all occupants age
        self.ages = np.array([i_age for i_age in self.ages if not death_function(i_age)]) # average of life expectancies 79 and 83
        self.household_size = len(self.ages)
        if self.household_size <= 0: # handle case no individuals left in property - return to options
            self.my_home.occupied = 0
            G = self.model.dynamic_neighbours
            G.remove_node((self.my_home.unique_id))
            self.model.space.occupied.remove(self.my_home.unique_id) # remove using building unique_id
        

        self.savings += self.income # agent earns money
        step_damage = depth_damage_calculation(self.my_home.inundation,self.my_home.area) # calculate damage
        self.flood_damage = step_damage # update flood damage to equal what was experienced that year
        neighbourhood_attributes = self.get_neighbourhood_attributes()
        
        # sample properties
        properties = self.sample_properties(self.model.house_sample_size) # number sampled is a model parameter
        property_evaluation = self.evaluate_properties(properties, neighbourhood_attributes)
        chosen_property = property_evaluation[0] # Building

        # return outcome of expected utility
        utility_case = self.expected_utility(
            savings= self.savings, 
            flood_preparedness=self.my_home.flood_preparedness, 
            property_value=self.my_home.property_value, 
            flood_level=self.my_home.inundation,
            damage=step_damage,
            neighbourhood_attributes=neighbourhood_attributes,
            destination=chosen_property,
            migration_cost = property_evaluation[1]
            )

        if self.my_home.flood_preparedness < self.my_home.inundation: # if flooded....
            self.floods_experienced += 1
            self.timesteps_since_last_flood = 0 # reset time since last flood to 0
        else: # else if damage was zero
            step_damage = 0 
            if self.floods_experienced > 1:
                self.timesteps_since_last_flood += 1 # add time since last flood

        match utility_case[0]:
            case 'nothing':

                if self.savings > step_damage: # if can afford to pay for damages, do so...
                    self.savings =- step_damage
                else:
                    self.my_home.property_value -= step_damage # otherwise, the property value gets damaged
            case 'adapt':
                cost = self.defence_cost(utility_case[1]) # calculates cost of defence
                self.adapt(cost[0],cost[1]) # 
            case 'migrate':
                self.migrate(chosen_property)

        

    def get_neighbourhood_attributes(self):
        
        # NOTE: neighbour network is by building, not the social network of households
        # get list of occupied building nodes connected to household agent
        # print(self.model.dynamic_neighbours.nodes)
        # print(len(self.model.dynamic_neighbours.nodes))
        
        neighbours = self.model.dynamic_neighbours.neighbors(self.my_home.unique_id) # calculate attributes for existing properties NOTE: look out for American spelling of neighbour for networkx function. 

        no = len(list(neighbours)) # number of neighbours

        if no == 0: # handle no neighbours case
            return [0,0,0,0,0]
        else:
            # calculate average flood preparedness, property value, inundation height
            fp,pv,ih = 0,0,0
            
            buildings = self.model.space._buildings
            household_ids = []
            for neighbour_id in neighbours:
                building = buildings.get(neighbour_id)
                fp+=building.flood_preparedness
                pv+=building.property_value
                ih+=building.inundation
                household_ids.append(building.household_id) # populate list of household_ids

            fp,pv,ih = fp/no,pv/no,ih/no # calculate averages
            
            # calculate average of floods experienced and timesteps since last flood

            fe,tslf = 0,0

            households = self.model.schedule._agents
            for household_id in household_ids:
                household = households[household_id]
                fe+=household.floods_experienced
                tslf+=household.timesteps_since_last_flood
            # return list of averages: 
            fe,tslf = fe/no,tslf/no
            # [flood prepardness, property value, inundation height, floods experienced, time since last flood]
            # to be accessed by indexing
            return [fp,pv,ih,fe,tslf]
        

    def defence_cost(self, height):
        length_of_wall = self.my_home.length

        # all costs in k£
        if height < 1.2:
            cost = length_of_wall*1.4
            wall_height = 1.2
        elif 1.2 < height < 2.1:
            cost = length_of_wall*2.9
            wall_height = 2.1
        elif 2.1 < height < 5.3:
            cost = length_of_wall*3.6
            wall_height = 5.3
        else:
            cost = length_of_wall*11.2
            wall_height = height
        
        # based on https://assets.publishing.service.gov.uk/media/6034ed2ed3bf7f264f23eb51/Cost_estimation_for_fluvial_defences.pdf, table 1.1

        return [cost, wall_height]


    def adapt(self, defence_cost, defence_height) -> None:
        self.savings -= defence_cost
        self.my_home.flood_preparedness = defence_height # assuming the height is 
        

    def sample_properties(self, num_properties):

        # return property value of new home to migration cost first before comitting - need to inspect attributes of flood prepardness, property value, area / household size ratio

        available_buildings = set(self.model.space.building_ids.difference(self.model.space.occupied))

        # Convert the set to a list for random.sample (if size of set is manageable)
        if len(available_buildings) <= num_properties:  # Check if set size is smaller or equal to desired sample size
            sampled_properties = list(available_buildings)  # Convert the entire set to a list
        else:
            sampled_properties = random.sample(list(available_buildings), num_properties)  # Sample from the set

        # Create a dictionary from sampled IDs and their corresponding buildings
        properties = {building_id: self.model.space._buildings.get(building_id) for building_id in sampled_properties}

        return properties


    def evaluate_properties(self, properties: dict, neighbourhood_attributes):
        '''
        Returns the property with the best cost and attributes
        '''
        # calculates fixed cost and variable migration costs

        current_point = Point(self.my_home.centroid)

        property_costs = {}
        cost_per_m = self.model.variable_migration_cost #k£ - variable cost that scales with distances
        # fixed_migration_cost in k£ - psychological cost of leaving current property

        n_flood_prep = neighbourhood_attributes[0]
        n_property_value = neighbourhood_attributes[1]
        n_inundation_height = neighbourhood_attributes[2]
        n_floods_experienced = neighbourhood_attributes[3]
        n_time_since_last_flood = neighbourhood_attributes[4]

        # for each property in sample, calculate the distance away and the property costs
        for property_id, property in properties.items():

            property_point = Point(property.centroid)         
            points_df = gpd.GeoDataFrame({'geometry': [current_point, property_point]},crs='EPSG:4326')
            points_df = points_df.to_crs("EPSG:27700")
            dist = points_df.geometry.iloc[0].distance(points_df.geometry.iloc[1]) # unit in metres between points
            # sum of property_value, variable distance-based cost and fixed cost
            property_costs[property_id] = self.model.space._buildings[property_id].property_value + dist*cost_per_m + self.model.fixed_migration_cost

        # take the property with minimum costs
        min_property_id = min(property_costs, key=property_costs.get)

        return [properties[min_property_id], property_costs[min_property_id]]

    def migrate(self, new_home) -> None:

        # update migration count, replaces old home with new one, and returns old home to pool of unoccupied homes

        self.model.migration_count += 1
        self.my_home.occupied = 0

        # drop old node from network

        G = self.model.dynamic_neighbours
        G.remove_node((self.my_home.unique_id))

        self.model.space.occupied.remove(self.my_home.unique_id) # remove using building unique_id
        self.set_home(new_home) # set building geoagent as new home

        # update network
        new_node = new_home.unique_id
        edges_to_copy = self.model.neighbours_lookup.edges(new_node) # a list of tuples (new_node, other_node)
        # print("new node is " + str(new_node) + " with nodes to add " + str(edges_to_copy))

        G.add_node(new_node) # add node first to handle island case

        for edge in edges_to_copy:

            # Add the edge only if node exists in graph
            if G.has_node(edge[1]):
                G.add_edge(new_node, edge[1])
                # print("added " + str(edge))
            # else:
                # print(" didn't add " + str(edge))

        # print("new graph is " + str(G.nodes))