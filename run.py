from coastal_model import CoastalModel
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

model = CoastalModel(100)
for i in range(70):
    model.step()

agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell_content, (x, y) in model.grid.coord_iter():
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count

# Plot using seaborn, with a size of 5x5
g = sns.heatmap(data = agent_counts, cmap="crest", annot=False, cbar=True, square=True)
g.set(title="Number of agents on each cell of the grid");

plt.show()