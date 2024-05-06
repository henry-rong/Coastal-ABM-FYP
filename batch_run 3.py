import mesa
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
# sns.set_theme(font_scale=1, rc={'text.usetex' : True})
from coastal_model.model import Population  # Assuming coastal_model is the package containing your Population model
import os

current_directory = os.getcwd()
os.chdir(current_directory)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

no_of_neighbours = 0

csv_file_path = f"..\\coastal_csvs\\results_{no_of_neighbours}_{timestamp}.csv"

params = {
    "people_per_household": 3.5,
    "neighbourhood_radius": no_of_neighbours,
    "initial_flood_experience": 0,
    "initial_flood_preparedness": 0,
    "house_sample_size": 3,
    "fixed_migration_cost": 50, #k£
    "household_adaptation_cost": 10 #k£
}

results = mesa.batch_run(
    Population,
    parameters=params,
    iterations=200,
    max_steps=69,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

results_df = pd.DataFrame(results)
print(results_df.keys())

results_filtered = results_df
results_filtered["Step"] += 2010
results_filtered.drop(columns=['AgentID'])
results_aggregated = results_filtered.groupby(["Step"]).mean().reset_index() # aggregate for Step (each year)
results_aggregated.to_csv(csv_file_path, index=False)

print("DataFrame successfully exported to CSV file:", csv_file_path)

migration_results_df = results_filtered.groupby(["iteration","Step", "neighbourhood_radius"]).agg({"Migration Count": "mean"}).reset_index()
migration_results_df.to_csv(f"..\\coastal_csvs\\migration_results_{no_of_neighbours}_{timestamp}.csv", index=False)
flood_results_df = results_filtered.groupby(["iteration","Step","neighbourhood_radius"]).agg({"Max Flood Inundation":"mean"}).reset_index()
flood_results_df.to_csv(f"..\\coastal_csvs\\flood_results_{no_of_neighbours}_{timestamp}.csv", index=False)
adaptation_results_df = results_filtered.groupby(["iteration","Step","neighbourhood_radius"]).agg({"Adaptation":"mean"}).reset_index()
adaptation_results_df.to_csv(f"..\\coastal_csvs\\adaptation_results_{no_of_neighbours}_{timestamp}.csv", index=False)
flood_dmg_results_df = results_filtered.groupby(["iteration","Step","neighbourhood_radius"]).agg({"Flood Damage":"mean"}).reset_index()
flood_dmg_results_df.to_csv(f"..\\coastal_csvs\\damage_results_{no_of_neighbours}_{timestamp}.csv", index=False)
flood_exp_results_df = results_filtered.groupby(["iteration","Step","neighbourhood_radius"]).agg({"Floods experienced":"mean"}).reset_index()
flood_exp_results_df.to_csv(f"..\\coastal_csvs\\exp_results_{no_of_neighbours}_{timestamp}.csv", index=False)
utility_nothing_results_df = results_filtered.groupby(["iteration","Step","neighbourhood_radius"]).agg({"Nothing utility":"mean"}).reset_index()
utility_nothing_results_df.to_csv(f"..\\coastal_csvs\\utility_nothing_results_{no_of_neighbours}_{timestamp}.csv", index=False)
utility_adapt_results_df = results_filtered.groupby(["iteration","Step","neighbourhood_radius"]).agg({"Adapt utility":"mean"}).reset_index()
utility_adapt_results_df.to_csv(f"..\\coastal_csvs\\utility_adapt_results_{no_of_neighbours}_{timestamp}.csv", index=False)
utility_migrate_results_df = results_filtered.groupby(["iteration","Step","neighbourhood_radius"]).agg({"Migrate utility":"mean"}).reset_index()
utility_migrate_results_df.to_csv(f"..\\coastal_csvs\\utility_migrate_results_{no_of_neighbours}_{timestamp}.csv", index=False)
saving_results_df = results_filtered.groupby(["iteration","Step","neighbourhood_radius"]).agg({"Savings":"mean"}).reset_index()
saving_results_df.to_csv(f"..\\coastal_csvs\\savings_results_{no_of_neighbours}_{timestamp}.csv", index=False)


ylabels = ["Migration Count (moves)", "Max Flood Inundation (m)", "Average flood defence height (m)","Average damage (£)","Number of households experiencing flooding","utility of nothing","utility of adapt","utility of migration","Savings"]
titles = ["Migration Count from 2010 to 2080", "Max Flood Inundation Rise from 2010 to 2080", "Flood Adaptation Change from 2010 to 2080","Average flood depth damage per year from 2010 to 2080","Average flood experience count per year from 2010 to 2080","utility of nothing","utility of adapt","utility of migration","Savings"]
ys = ["Migration Count", "Max Flood Inundation", "Adaptation","Flood Damage","Floods experienced","Nothing utility","Adapt utility","Migrate utility","Savings"]
data_sources = [migration_results_df, flood_results_df, adaptation_results_df,flood_dmg_results_df,flood_exp_results_df,utility_nothing_results_df,utility_adapt_results_df,utility_migrate_results_df,saving_results_df]

for i in range(len(data_sources)): 

    plt.figure(i)
    fig, axes = plt.subplots(figsize=(7, 5))
 
    sns.lineplot(data=data_sources[i], ax=axes, x="Step", y=ys[i], hue="neighbourhood_radius", palette="dark:#5A9_r")
    axes.set(
        xlabel="Year",
        ylabel=ylabels[i],
        title=titles[i],
    )


plt.show()

