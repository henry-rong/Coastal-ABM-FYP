import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],  # Specify your preferred font here
})

sns.set_style("whitegrid")

path = "..\\coastal_csvs\\10_iters\\results_neighbourhood_radius_2024-05-08_13-37-23.csv"

current_directory = os.getcwd()
os.chdir(current_directory)

results_df = pd.read_csv(f"{path}")


results_filtered = results_df
results_filtered.drop(columns=['AgentID','RunId'], inplace=True)

print(results_filtered.keys())

results_aggregated = results_filtered.groupby(["iteration","Step"]).mean().reset_index() # aggregate for Step (each year)

print(results_aggregated.keys())

ylabels = ["Migration Count", "Max Inundation (m)", "Mean defence height (m)","Mean damage (k£)","Flood experience","Savings (k£)","Income (k£)","Utility of inaction","Utility of adaptation","Utility of migration"]
ys = ["Migration Count", "Max Flood Inundation", "Adaptation","Flood Damage","Floods experienced","Savings","Income","Nothing Utility","Adapt Utility","Migrate Utility"] # the actual column being accessed
# Assuming combined_dfs is defined as in your code

fig, axes = plt.subplots(5,2,figsize=(6, 8),sharex=True)

for row in range(5):

    for col in range(2):      

        index = int((col)+(2*row))
        # print(index)

        sns.lineplot(data=results_aggregated, ax=axes[row,col], x="Step", y=ys[index])


        print("for index " + str(index) + " ys is " + ys[index] + " and its ylabel is " + ylabels[index] + " at position (" + str(row) + "," + str(col) + ")")

        axes[row,col].set(
            xlabel="Year",
            ylabel=ylabels[index],
        )

    
plt.tight_layout()
plt.show()
plt.savefig(f"..\\coastal_pngs\\plot_iter10_{timestamp}.png")