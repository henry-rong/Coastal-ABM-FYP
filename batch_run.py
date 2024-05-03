import mesa
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(font_scale=1, rc={'text.usetex' : True})


from coastal_model.model import Population

params = {
    "people_per_household": range(3,5,1),
    "neighbourhood_radius": range(25,75,25),
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
    iterations=2,
    max_steps=69,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

results_df = pd.DataFrame(results)
print(results_df.keys())

# Filter the results to only contain the data of one agent at the final step of each episode
# results_filtered = results_df[(results_df.AgentID == 0)]
results_filtered = results_df
results_filtered[["iteration","Step", "Max Flood Inundation", "Migration Count",'Adaptation','people_per_household',"neighbourhood_radius"]].reset_index(drop=True)
results_filtered["Step"] += 2010
# results_filtered["iteration"] += 1

# aggregate data
migration_results_df = (results_filtered.groupby(["iteration","people_per_household","Step","neighbourhood_radius"]).agg({"Migration Count":"mean"}).reset_index())
flood_results_df = (results_filtered.groupby(["iteration","people_per_household","Step","neighbourhood_radius"]).agg({"Max Flood Inundation":"mean"}).reset_index())
adaptation_results_df = (results_filtered.groupby(["iteration","people_per_household","Step","neighbourhood_radius"]).agg({"Adaptation":"mean"}).reset_index())

ylabels = ["Migration Count (moves)","Max Flood Inundation (m)","Average flood defence height (m)"]
titles = ["Migration Count from 2010 to 2080","Max Flood Inundation Rise from 2010 to 2080","Flood Adaptation Change from 2010 to 2080"]
ys = ["Migration Count","Max Flood Inundation","Adaptation"]
data_sources = [migration_results_df,flood_results_df]

plt.figure(0)

fig, axes = plt.subplots(2, 1, figsize=(15, 5), sharex=True)

for i in range(2):  
    sns.lineplot(data=data_sources[i], ax=axes[i], x="Step", y=ys[i], hue="people_per_household", palette="dark:#5A9_r")
    axes[i].set(
        xlabel="Year",
        ylabel=ylabels[i],
        title=titles[i],
    )

plt.figure(1)

fig, axes = plt.subplots(figsize=(15, 5))

sns.lineplot(data=adaptation_results_df, ax=axes, x="Step", y=ys[2], hue="people_per_household", palette="dark:#5A9_r")
axes.set(
    xlabel="Year",
    ylabel=ylabels[2],
    title=titles[2]
)

plt.figure(2)

fig, axes = plt.subplots(2, 1, figsize=(15, 5), sharex=True)

for i in range(2):  
    sns.lineplot(data=data_sources[i], ax=axes[i], x="Step", y=ys[i], hue="neighbourhood_radius", palette="dark:#5A9_r")
    axes[i].set(
        xlabel="Year",
        ylabel=ylabels[i],
        title=titles[i],
    )

plt.figure(3)

fig, axes = plt.subplots(figsize=(15, 5))

sns.lineplot(data=adaptation_results_df, ax=axes, x="Step", y=ys[2], hue="neighbourhood_radius", palette="dark:#5A9_r")
axes.set(
    xlabel="Year",
    ylabel=ylabels[2],
    title=titles[2]
)

plt.show()