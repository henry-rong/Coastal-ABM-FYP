import mesa
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



from coastal_model.model import Population

params = {}

results = mesa.batch_run(
    Population,
    parameters=params,
    iterations=10,
    max_steps=80,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

results_df = pd.DataFrame(results)
print(results_df.keys())

# Index(['RunId', 'iteration', 'Step', 'Sea Level', 'Migration Count', 'AgentID','Adaptation'],dtype='object')

# Filter the results to only contain the data of one agent (the Gini coefficient will be the same for the entire population at any time) at the 100th step of each episode
# results_filtered = results_df[(results_df.AgentID == 0)]
results_filtered = results_df
results_filtered[["iteration","Step", "Sea Level", "Migration Count",'Adaptation']].reset_index(
    drop=True
)  # Create a scatter plot
results_filtered["Step"] += 2020
# results_filtered["iteration"] += 1


fig, axes = plt.subplots(2, 1,figsize=(15, 5),sharex=True)

sns.lineplot(data=results_filtered,ax=axes[0], x="Step", y="Migration Count",hue="iteration")
axes[0].set(
    xlabel="Year",
    ylabel="Migration Count (moves)",
    title="Migration Count from 2020 to 2100",
);

sns.lineplot(data=results_filtered,ax=axes[1], x="Step", y="Sea Level",hue="iteration")
axes[1].set(
    xlabel="Year",
    ylabel="Sea Level (m)",
    title="Sea Level Rise from 2020 to 2100",
);



plt.show()