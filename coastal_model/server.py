import mesa
import mesa_geo as mg
from shapely.geometry import Point, Polygon

from .model import Population
from .space import CoastalCell


class NumAgentsElement(mesa.visualization.TextElement):
    def __init__(self):
        super().__init__()

    def render(self, model):
        return f"Number of Agents: {len(model.space.agents)}"


def agent_portrayal(agent):
    if isinstance(agent, mg.GeoAgent):
        if isinstance(agent.geometry, Point):
            return {
                "stroke": False,
                "color": "Green",
                "radius": 2,
                "fillOpacity": 0.3,
            }
        elif isinstance(agent.geometry, Polygon):
            return {
                "fillColor": "Blue",
                "fillOpacity": 1,
            }
    elif isinstance(agent, CoastalCell):
        return (agent.population, agent.population, agent.population, 1)


geospace_element = mg.visualization.MapModule(agent_portrayal,map_width=700)
num_agents_element = NumAgentsElement()

server = mesa.visualization.ModularServer(
    Population, [geospace_element, num_agents_element], "Population Model"
)