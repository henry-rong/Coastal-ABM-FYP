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
        return f"Number of Agents: {len(model.space.agents)}  Migration Count: {model.migration_count}"

def agent_portrayal(agent):

# options: https://github.com/projectmesa/mesa-geo/blob/main/mesa_geo/visualization/modules/MapVisualization.py

    # if isinstance(agent, Household):
    #     portrayal = {"stroke": False,"color": "Green", "fillOpacity": 0.3, "radius": 2}
    #     portrayal["color"] = "Red" if agent.flood_preparedness < 0.5 else "Green"
    #     portrayal["radius"] = 1 if agent.flood_preparedness < 0.5 else 2
    #     return portrayal
        
    # elif isinstance(agent, CoastalArea):
    #     return {
    #         "fillColor": "Blue",
    #         "fillOpacity": 1,
    #     }
    
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

        # elif isinstance(agent.geometry, Point):
        # elif isinstance(agent, Household):
        #     portrayal = {"stroke": False,"color": "Green", "fillOpacity": 0.3, "radius": 2}
        #     portrayal["color"] = "Red" if agent.flood_preparedness < 0.5 else "Green"
        #     portrayal["radius"] = 1 if agent.flood_preparedness < 0.5 else 2
        #     return portrayal
        
        elif isinstance(agent.geometry, Polygon):
            return {
                "fillColor": "#ADD8E6",
                "fillOpacity": 1,
                "stroke": True,
                "color": "Black",
                "opacity": 1,
                "weight": 1,
            }


    # elif isinstance(agent, CoastalCell): # visualises the raster layer
    #     return (agent.population, agent.population, agent.population, 1)
    



geospace_element = mg.visualization.MapModule(agent_portrayal,map_width=700)
num_agents_element = NumAgentsElement()
chart1 = mesa.visualization.ChartModule([{"Label": "Sea Level", "Color": "Black"}], data_collector_name="datacollector")
chart2 = mesa.visualization.ChartModule([{"Label": "Migration Count", "Color": "Red"}], data_collector_name="datacollector")
server = mesa.visualization.ModularServer(Population, [geospace_element, num_agents_element, chart1,chart2], "Population Model")