import mesa
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



from coastal_model.model import Population

params = {
    "people_per_household": 3.5,
    "neighbourhood_radius": 50,
    "initial_flood_experience": 0,
    "initial_flood_preparedness": 0,
    "house_sample_size": 3,
    "fixed_migration_cost": 50, #k£
    "household_adaptation_cost": 10 #k£
          }

# params = {
#     "people_per_household": range(1,4),
#     "neighbourhood_radius": range(0,50,10),
#     "initial_flood_experience": range(0,1),
#     "initial_flood_preparedness": range(0,1),
#     "house_sample_size": range(1,5),
#     "fixed_migration_cost": range(50,100,25), #k£
#     "household_adaptation_cost": range(1,10) #k£
#           }

results = mesa.batch_run(
    Population,
    parameters=params,
    iterations=1,
    max_steps=69,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

results_df = pd.DataFrame(results)
print(results_df.keys())

# Index(['RunId', 'iteration', 'Step', 'Max Flood Inundation', 'Migration Count', 'AgentID','Adaptation'],dtype='object')

# Filter the results to only contain the data of one agent at the final step of each episode
# results_filtered = results_df[(results_df.AgentID == 0)]
results_filtered = results_df
results_filtered[["iteration","Step", "Max Flood Inundation", "Migration Count",'Adaptation']].reset_index(
    drop=True
)  # Create a scatter plot
results_filtered["Step"] += 2010
# results_filtered["iteration"] += 1


fig, axes = plt.subplots(2, 1,figsize=(15, 5),sharex=True)

sns.lineplot(data=results_filtered,ax=axes[0], x="Step", y="Migration Count",hue="iteration")
axes[0].set(
    xlabel="Year",
    ylabel="Migration Count (moves)",
    title="Migration Count from 2010 to 2080",
);

sns.lineplot(data=results_filtered,ax=axes[1], x="Step", y="Max Flood Inundation",hue="iteration")
axes[1].set(
    xlabel="Year",
    ylabel="Max Flood Inundation (m)",
    title="Max Flood Inundation Rise from 2010 to 2080",
);



plt.show()