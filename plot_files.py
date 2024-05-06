import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# plt.rcParams.update({
#     # "text.usetex": True,
#     "font.family": "serif",
#     "font.serif": ["Times New Roman"],  # Specify your preferred font here
# })

sns.set_style("whitegrid")



current_directory = os.getcwd()
os.chdir(current_directory)

migration_results_0_df = pd.read_csv(f"..\\coastal_csvs\\migration_results_0_2024-05-06_01-23-42.csv")
migration_results_25_df = pd.read_csv(f"..\\coastal_csvs\\migration_results_25_2024-05-06_01-21-12.csv")
migration_results_50_df = pd.read_csv(f"..\\coastal_csvs\\migration_results_50_2024-05-06_01-20-26.csv")

flood_results_0_df = pd.read_csv(f"..\\coastal_csvs\\flood_results_0_2024-05-06_01-23-42.csv")
flood_results_25_df = pd.read_csv(f"..\\coastal_csvs\\flood_results_25_2024-05-06_01-21-12.csv")
flood_results_50_df = pd.read_csv(f"..\\coastal_csvs\\flood_results_50_2024-05-06_01-20-26.csv")

adaptation_results_0_df = pd.read_csv(f"..\\coastal_csvs\\adaptation_results_0_2024-05-06_01-23-42.csv")
adaptation_results_25_df = pd.read_csv(f"..\\coastal_csvs\\adaptation_results_25_2024-05-06_01-21-12.csv")
adaptation_results_50_df = pd.read_csv(f"..\\coastal_csvs\\adaptation_results_50_2024-05-06_01-20-26.csv")

flood_dmg_results_0_df = pd.read_csv(f"..\\coastal_csvs\\damage_results_0_2024-05-06_01-23-42.csv")
flood_dmg_results_25_df = pd.read_csv(f"..\\coastal_csvs\\damage_results_25_2024-05-06_01-21-12.csv")
flood_dmg_results_50_df = pd.read_csv(f"..\\coastal_csvs\\damage_results_50_2024-05-06_01-20-26.csv")

# flood_exp_results_0_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_0_2024-05-06_01-23-42.csv")
# flood_exp_results_25_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_25_2024-05-06_01-21-12.csv")
# flood_exp_results_50_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_50_2024-05-06_01-20-26.csv")

# cost_nothing_results_0_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_{no_of_neighbours}_{timestamp}.csv", index=False)

# cost_adapt_results_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_{no_of_neighbours}_{timestamp}.csv", index=False)

# cost_migrate_results_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_{no_of_neighbours}_{timestamp}.csv", index=False)

# saving_results_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_{no_of_neighbours}_{timestamp}.csv", index=False)


# plt.figure(1)
# fig, axes = plt.subplots(figsize=(7, 5))

# sns.lineplot(data=adaptation_results_df, ax=axes, x="Step", y="Flood Damage", hue="neighbourhood_radius", palette="dark:#5A9_r")
# axes.set(
#     xlabel="Year",
#     ylabel="Average flood defence height (m)",
#     title="Flood Adaptation change from 2010 to 2080",
# )

ylabels = ["Migration Count (moves)", "Max Flood Inundation (m)", "Average flood defence height (m)","Average damage (k£)"]
titles = ["Migration Count from 2010 to 2080", "Max Flood Inundation Rise from 2010 to 2080", "Flood Adaptation Change from 2010 to 2080","Average flood depth damage per year from 2010 to 2080"]
ys = ["Migration Count", "Max Flood Inundation", "Adaptation","Flood Damage"]
# ylabels = ["Migration Count (moves)", "Max Flood Inundation (m)", "Average flood defence height (m)","Average damage (k£)","Number of households experiencing flooding"]
# titles = ["Migration Count from 2010 to 2080", "Max Flood Inundation Rise from 2010 to 2080", "Flood Adaptation Change from 2010 to 2080","Average flood depth damage per year from 2010 to 2080","Average flood experience count per year from 2010 to 2080"]
# ys = ["Migration Count", "Max Flood Inundation", "Adaptation","Flood Damage","Floods experienced"]
# data_sources_0 = [migration_results_0_df, flood_results_0_df, adaptation_results_0_df,flood_dmg_results_0_df,flood_exp_results_0_df]
# data_sources_25 = [migration_results_25_df, flood_results_25_df, adaptation_results_25_df,flood_dmg_results_25_df,flood_exp_results_25_df]
# data_sources_50 = [migration_results_50_df, flood_results_50_df, adaptation_results_50_df,flood_dmg_results_50_df,flood_exp_results_50_df]
data_sources_0 = [migration_results_0_df, flood_results_0_df, adaptation_results_0_df,flood_dmg_results_0_df]
data_sources_25 = [migration_results_25_df, flood_results_25_df, adaptation_results_25_df,flood_dmg_results_25_df]
data_sources_50 = [migration_results_50_df, flood_results_50_df, adaptation_results_50_df,flood_dmg_results_50_df]
data_sources = [data_sources_0,data_sources_25,data_sources_50]


# Merge dataframes within each data_sources_x list along 'Iteration' and 'Steps'
merged_data_sources_0 = pd.merge(data_sources_0[0], data_sources_0[1], on=['iteration', 'Step','neighbourhood_radius'])
for df in data_sources_0[2:]:
    merged_data_sources_0 = pd.merge(merged_data_sources_0, df, on=['iteration', 'Step','neighbourhood_radius'])

merged_data_sources_25 = pd.merge(data_sources_25[0], data_sources_25[1], on=['iteration', 'Step','neighbourhood_radius'])
for df in data_sources_25[2:]:
    merged_data_sources_25 = pd.merge(merged_data_sources_25, df, on=['iteration', 'Step','neighbourhood_radius'])

merged_data_sources_50 = pd.merge(data_sources_50[0], data_sources_50[1], on=['iteration', 'Step','neighbourhood_radius'])
for df in data_sources_50[2:]:
    merged_data_sources_50 = pd.merge(merged_data_sources_50, df, on=['iteration', 'Step','neighbourhood_radius'])

# Merge the resulting dataframes from each data_sources_x list together
final_merged_df = pd.concat([merged_data_sources_0, merged_data_sources_25, merged_data_sources_50], ignore_index=True)

print(final_merged_df.head)

final_merged_df.to_csv(f"..\\coastal_csvs\\final_combined_df_{timestamp}.csv", index=False)

# Assuming combined_dfs is defined as in your code
for result in range(len(data_sources_0)):
    plt.figure(result)
    fig, axes = plt.subplots(figsize=(7, 3))

    sns.lineplot(data=final_merged_df, ax=axes, x="Step", y=ys[result], hue="neighbourhood_radius", style="neighbourhood_radius",palette="dark")

    axes.set(
        xlabel="Year",
        ylabel=ylabels[result],
        title=titles[result],
    )

    plt.legend(title="Distanceband (m)", loc="lower right")
    plt.tight_layout()
    plt.savefig(f"..\\coastal_pngs\\plot_{ys[result]}_{timestamp}.png")

plt.show()