import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
plt.rcParams.update({
    # "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],  # Specify your preferred font here
})

current_directory = os.getcwd()
os.chdir(current_directory)

# migration_results_df = pd.read_csv(f"..\\coastal_csvs\\migration_results_2024-05-05_18-15-30.csv")
# flood_results_df = pd.read_csv(f"..\\coastal_csvs\\flood_results_2024-05-05_18-15-30.csv")
# adaptation_results_df = pd.read_csv(f"..\\coastal_csvs\\adaptation_results_2024-05-05_18-15-30.csv")
# flood_dmg_results_df = pd.read_csv(f"..\\coastal_csvs\\damage_results_2024-05-05_18-15-30.csv")
# flood_exp_results_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_2024-05-05_18-15-30.csv")

adaptation_results_df = pd.read_csv(f"..\\coastal_csvs\\damage_results_50_2024-05-05_19-33-05.csv")

plt.figure(1)
fig, axes = plt.subplots(figsize=(7, 5))

sns.lineplot(data=adaptation_results_df, ax=axes, x="Step", y="Flood Damage", hue="neighbourhood_radius", palette="dark:#5A9_r")
axes.set(
    xlabel="Year",
    ylabel="Average flood defence height (m)",
    title="Flood Adaptation change from 2010 to 2080",
)

# ylabels = ["Migration Count (moves)", "Max Flood Inundation (m)", "Average flood defence height (m)","Average damage (£)","Number of households experiencing flooding"]
# titles = ["Migration Count from 2010 to 2080", "Max Flood Inundation Rise from 2010 to 2080", "Flood Adaptation Change from 2010 to 2080","Average flood depth damage per year from 2010 to 2080","Average flood experience count per year from 2010 to 2080"]
# ys = ["Migration Count", "Max Flood Inundation", "Adaptation","Flood Damage","Floods experienced"]
# data_sources = [migration_results_df, flood_results_df, adaptation_results_df,flood_dmg_results_df,flood_exp_results_df]

# for i in range(len(data_sources)): 

#     plt.figure(i)
#     fig, axes = plt.subplots(figsize=(7, 5))
 
#     sns.lineplot(data=data_sources[i], ax=axes, x="Step", y=ys[i], hue="neighbourhood_radius", palette="dark:#5A9_r")
#     axes.set(
#         xlabel="Year",
#         ylabel=ylabels[i],
#         title=titles[i],
#     )

#     plt.plot(data_sources[i]["Step"], data_sources[i][ys[i]]["mean"], marker='o', label="Mean")

#     # Plot error bars for upper and lower bounds (max and min)
#     plt.errorbar(data_sources[i]["Step"], data_sources[i][ys[i]]["mean"],
#                 yerr=[data_sources[i][ys[i]]["mean"] - data_sources[i][ys[i]]["min"],
#                     data_sources[i][ys[i]]["max"] - data_sources[i][ys[i]]["mean"]],
#                 fmt='none', ecolor='gray', capsize=5, label="Max-Min Range")


plt.show()
