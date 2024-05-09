import mesa
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from multiprocessing import freeze_support
sns.set_style("whitegrid")
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],  # Specify your preferred font here
})
from coastal_model.model import CoastalModel
import os

current_directory = os.getcwd()
os.chdir(current_directory)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

data_label = "fixed_migration_cost"

csv_file_path = f"..\\coastal_csvs\\results_{data_label}_{timestamp}.csv"

params = {
    "neighbourhood_radius": 25,
    "initial_flood_experience": 0,
    "initial_flood_preparedness": 4, # the return period protection standard at 2010, ranging with all 9 
    "house_sample_size": 3,
    "savings_mean": 40,
    "income_mean": 30,
    "fixed_migration_cost": [0,5,10], #k£
    "variable_migration_cost": 0.001 #k£ per m
}

results = mesa.batch_run(
    CoastalModel,
    parameters=params,
    iterations=3,
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

migration_results_df = results_filtered.groupby(["iteration","Step", data_label]).agg({"Migration Count": "mean"}).reset_index()
migration_results_df.to_csv(f"..\\coastal_csvs\\migration_results_{data_label}_{timestamp}.csv", index=False)
flood_results_df = results_filtered.groupby(["iteration","Step",data_label]).agg({"Max Flood Inundation":"mean"}).reset_index()
flood_results_df.to_csv(f"..\\coastal_csvs\\flood_results_{data_label}_{timestamp}.csv", index=False)
adaptation_results_df = results_filtered.groupby(["iteration","Step",data_label]).agg({"Adaptation":"mean"}).reset_index()
adaptation_results_df.to_csv(f"..\\coastal_csvs\\adaptation_results_{data_label}_{timestamp}.csv", index=False)
flood_dmg_results_df = results_filtered.groupby(["iteration","Step",data_label]).agg({"Flood Damage":"mean"}).reset_index()
flood_dmg_results_df.to_csv(f"..\\coastal_csvs\\damage_results_{data_label}_{timestamp}.csv", index=False)
flood_exp_results_df = results_filtered.groupby(["iteration","Step",data_label]).agg({"Floods experienced":"mean"}).reset_index()
flood_exp_results_df.to_csv(f"..\\coastal_csvs\\exp_results_{data_label}_{timestamp}.csv", index=False)
utility_nothing_results_df = results_filtered.groupby(["iteration","Step",data_label]).agg({"Nothing Utility":"mean"}).reset_index()
utility_nothing_results_df.to_csv(f"..\\coastal_csvs\\utility_nothing_results_{data_label}_{timestamp}.csv", index=False)
utility_adapt_results_df = results_filtered.groupby(["iteration","Step",data_label]).agg({"Adapt Utility":"mean"}).reset_index()
utility_adapt_results_df.to_csv(f"..\\coastal_csvs\\utility_adapt_results_{data_label}_{timestamp}.csv", index=False)
utility_migrate_results_df = results_filtered.groupby(["iteration","Step",data_label]).agg({"Migrate Utility":"mean"}).reset_index()
utility_migrate_results_df.to_csv(f"..\\coastal_csvs\\utility_migrate_results_{data_label}_{timestamp}.csv", index=False)
saving_results_df = results_filtered.groupby(["iteration","Step",data_label]).agg({"Savings":"mean"}).reset_index()
saving_results_df.to_csv(f"..\\coastal_csvs\\savings_results_{data_label}_{timestamp}.csv", index=False)


ylabels = ["Migration Count (moves)", "Max Flood Inundation (m)", "Average flood defence height (m)","Average damage (k£)","Number of households experiencing flooding","Utility of nothing","Utility of adapt","Utility of migration","Savings"]
titles = ["Migration Count from 2010 to 2080", "Max Flood Inundation Rise from 2010 to 2080", "Flood Adaptation Change from 2010 to 2080","Average flood depth damage per year from 2010 to 2080","Average flood experience count per year from 2010 to 2080","Utility of nothing","Utility of adapt","Utility of migration","Savings"]
ys = ["Migration Count", "Max Flood Inundation", "Adaptation","Flood Damage","Floods experienced","Nothing Utility","Adapt Utility","Migrate Utility","Savings"]
data_sources = [migration_results_df, flood_results_df, adaptation_results_df,flood_dmg_results_df,flood_exp_results_df,utility_nothing_results_df,utility_adapt_results_df,utility_migrate_results_df,saving_results_df]
hues = ["neighbourhood_radius","initial_flood_experience","initial_flood_preparedness","house_sample_size","fixed_migration_cost","household_adaptation_cost"]


for i in range(len(data_sources)): 

    plt.figure(i)
    fig, axes = plt.subplots(figsize=(7, 5))

    sns.lineplot(data=data_sources[i], ax=axes, x="Step", y=ys[i], hue=data_label, palette="dark")
    axes.set(
        xlabel="Year",
        ylabel=ylabels[i],
        title=titles[i],
    )
    plt.legend(title=data_label, loc="lower right")
    plt.tight_layout()
    plt.savefig(f"..\\coastal_pngs\\plot_{ys[i]}_{timestamp}.png")


plt.show()