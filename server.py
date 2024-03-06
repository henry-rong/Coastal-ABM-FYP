from matplotlib.figure import Figure
from coastal_model import CoastalModel, mesa
import math
import numpy as np

coast = np.genfromtxt(f'maps/levels.txt') # 0 is water, 1-3 is land
x = np.shape(coast)[0]
y = np.shape(coast)[1]

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 1, "Layer": 0}
    portrayal["Color"] = "red" if agent.flood_preparedness < 0.5 else "green"
    portrayal["r"] = 0.5 if agent.flood_preparedness < 0.5 else 1
    return portrayal

model_params = {
    "N": mesa.visualization.Slider(
        value = 50,
        name = "Number of agents:",
        min_value =10,
        max_value =100,
        step = 1,
        description="Choose how many agents to include in the model",
    )
}

def make_histogram(model):
    # Note: you must initialize a figure using this method instead of
    # plt.figure(), for thread safety purpose
    fig = Figure()
    ax = fig.subplots()
    adaptation = [agent.flood_preparedness for agent in model.schedule.agents]
    # Note: you have to use Matplotlib's OOP API instead of plt.hist
    # because plt.hist is not thread-safe.
    ax.set_xlabel("Flood defenses")
    ax.set_ylabel("Number of agents")
    ax.hist(adaptation, bins=math.ceil(math.sqrt(len(adaptation))))
    fig.suptitle("Number of agents with flood defenses")

scale = 6

grid = mesa.visualization.CanvasGrid(agent_portrayal, x, y, scale*x, scale*y)
chart = mesa.visualization.ChartModule([{"Label": "Sea Level", "Color": "Black"}], data_collector_name="datacollector")

server = mesa.visualization.ModularServer(model_cls = CoastalModel, visualization_elements=[grid, chart], name= "Coastal Model", model_params=model_params)
server.port = 8521  # the default
server.launch()