import mesa
import mesa_geo as mg
from shapely.geometry import Point, Polygon
from .model import CoastalModel  # Assuming model.py is in the same directory
from .space import CoastalCell, CoastalArea  # Assuming space.py is in the same directory
from agent.building import Building

class NumAgentsElement(mesa.visualization.TextElement):
    def __init__(self):
        super().__init__()

    def render(self, model):
        return f"Number of Agents: {model.num_agents}  Migration Count: {model.migration_count}"

def agent_portrayal(agent):
    if isinstance(agent, mg.GeoAgent):
        if isinstance(agent, Building):
            portrayal = {
                "fillColor": "Black",
                "stroke": True,
                "color": "Black",
                "opacity": 0.5,
                "weight": 1,
                "fillOpacity": 1,
            }
            portrayal["fillColor"] = "White" if agent.occupied == 0 else ("#ff5226" if agent.flood_preparedness < agent.inundation else "#20f720")
            return portrayal
        elif isinstance(agent.geometry, Polygon):
            return {
                "fillColor": "#ADD8E6",
                "fillOpacity": 1,
                "stroke": True,
                "color": "Black",
                "opacity": 1,
                "weight": 1,
            }

model_params = {
    "data_label": "visual",
    "neighbourhood_radius": 25,
    "initial_flood_experience": 0,
    "initial_flood_preparedness": 4, # the return period protection standard at 2010, ranging with all 9 
    "house_sample_size": 3,
    "savings_mean": 40,
    "income_mean": 30,
    "fixed_migration_cost": 5, #k£
    "variable_migration_cost": 0.001 #k£ per m
}

geospace_element = mg.visualization.MapModule(agent_portrayal, map_width=700)
num_agents_element = NumAgentsElement()
chart1 = mesa.visualization.ChartModule([{"Label": "Max Flood Inundation", "Color": "Black"}], data_collector_name="datacollector")
chart2 = mesa.visualization.ChartModule([{"Label": "Migration Count", "Color": "Red"}], data_collector_name="datacollector")
server = mesa.visualization.ModularServer(CoastalModel, [geospace_element, num_agents_element, chart1, chart2], "CoastalModel", model_params)
