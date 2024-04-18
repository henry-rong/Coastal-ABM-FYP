import mesa
import mesa_geo as mg
from shapely.geometry import Point, Polygon

from .model import Population
from .space import CoastalCell, CoastalArea
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
                "fillColor":"Black",
                "stroke": True,
                "color": "Black",
                "opacity": 0.5,
                "weight": 1,
                "fillOpacity": 1,
            }

            portrayal["fillColor"] = "White" if agent.occupied == 0 else ("#ff5226" if agent.flood_preparedness < 0.5 else "#20f720")

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

model_params = {}

geospace_element = mg.visualization.MapModule(agent_portrayal,map_width=700)
num_agents_element = NumAgentsElement()
chart1 = mesa.visualization.ChartModule([{"Label": "Max Flood Inundation", "Color": "Black"}], data_collector_name="datacollector")
chart2 = mesa.visualization.ChartModule([{"Label": "Migration Count", "Color": "Red"}], data_collector_name="datacollector")
server = mesa.visualization.ModularServer(Population, [geospace_element, num_agents_element, chart1,chart2], "Population Model",model_params)