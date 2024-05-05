import mesa
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# sns.set_theme(font_scale=1, rc={'text.usetex' : True})
from coastal_model.model import Population  # Assuming coastal_model is the package containing your Population model
import os

current_directory = os.getcwd()
os.chdir(current_directory)

params = {
    "people_per_household": 3.5,
    "neighbourhood_radius": range(25, 75, 25),
    "initial_flood_experience": 0,
    "initial_flood_preparedness": 0,
    "house_sample_size": 3,
    "fixed_migration_cost": 50, #k£
    "household_adaptation_cost": 10 #k£
}

results = mesa.batch_run(
    Population,
    parameters=params,
    iterations=20,
    max_steps=69,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

results_df = pd.DataFrame(results)
print(results_df.keys())

results_filtered = results_df
results_filtered["Step"] += 2010

migration_results_df = results_filtered.groupby(["iteration","people_per_household","Step","neighbourhood_radius"]).agg({"Migration Count":"mean"}).reset_index()
flood_results_df = results_filtered.groupby(["iteration","people_per_household","Step","neighbourhood_radius"]).agg({"Max Flood Inundation":"mean"}).reset_index()
adaptation_results_df = results_filtered.groupby(["iteration","people_per_household","Step","neighbourhood_radius"]).agg({"Adaptation":"mean"}).reset_index()

ylabels = ["Migration Count (moves)", "Max Flood Inundation (m)", "Average flood defence height (m)"]
titles = ["Migration Count from 2010 to 2080", "Max Flood Inundation Rise from 2010 to 2080", "Flood Adaptation Change from 2010 to 2080"]
ys = ["Migration Count", "Max Flood Inundation", "Adaptation"]
data_sources = [migration_results_df, flood_results_df]

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
