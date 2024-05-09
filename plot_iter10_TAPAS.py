import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from datetime import datetime
import matplotlib.gridspec as gridspec


timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")



sns.set_style("whitegrid")

path = "..\\coastal_csvs\\10_iters\\results_neighbourhood_radius_2024-05-08_13-37-23.csv"

current_directory = os.getcwd()
os.chdir(current_directory)

results_df = pd.read_csv(f"{path}")
unity_results = pd.read_csv(f"..\\coastal_csvs\\results_unit_discount_2024-05-08_21-50-07.csv")

results_filtered = results_df
results_filtered.drop(columns=['AgentID','RunId'], inplace=True)
unity_filtered = unity_results
unity_filtered.drop(columns=['AgentID','RunId','data_label'], inplace=True)

unity_aggregated = unity_filtered.groupby(["iteration","Step"]).mean().reset_index()
results_aggregated = results_filtered.groupby(["iteration","Step"]).mean().reset_index()

ylabels = ["Migration Count", "Max Inundation (m)", "Mean defence height (m)","Mean damage (k£)","Flood experience","Savings (k£)","Income (k£)","Utility of inaction","Utility of adaptation","Utility of migration"]
ys = ["Max Flood Inundation", "Adaptation","Flood Damage","Floods experienced","Savings","Income","Nothing Utility","Adapt Utility","Migrate Utility","Migration Count"] # the actual column being accessed


# Define the layout using GridSpec
fig = plt.figure(figsize=(10, 8))
gs = gridspec.GridSpec(4, 6, figure=fig)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],  # Specify your preferred font here
})

# Define subplots for each section of the grid
ax1 = fig.add_subplot(gs[0, 1:3])  # First row, first two columns
ax2 = fig.add_subplot(gs[0, 3:5])  # First row, last two columns
ax3 = fig.add_subplot(gs[1, 0:2])   # Second row, first column
ax4 = fig.add_subplot(gs[1, 2:4])   # Second row, second column
ax5 = fig.add_subplot(gs[1, 4:6])   # Second row, third column
ax6 = fig.add_subplot(gs[2, 1:3])   
ax7 = fig.add_subplot(gs[2, 3:5])   
ax8 = fig.add_subplot(gs[3, 1:3])  
ax9 = fig.add_subplot(gs[3, 3:5])  

# Seaborn plots
sns.lineplot(data=results_aggregated, ax=ax1, x="Step", y="Max Flood Inundation")
sns.lineplot(data=results_aggregated, ax=ax2, x="Step", y="Income",label="Discounted")
sns.lineplot(data=results_aggregated, ax=ax3, x="Step", y="Nothing Utility")
sns.lineplot(data=results_aggregated, ax=ax4, x="Step", y="Adapt Utility")
sns.lineplot(data=results_aggregated, ax=ax5, x="Step", y="Migrate Utility")
sns.lineplot(data=results_aggregated, ax=ax6, x="Step", y="Floods experienced")
sns.lineplot(data=results_aggregated, ax=ax7, x="Step", y="Flood Damage")
sns.lineplot(data=results_aggregated, ax=ax8, x="Step", y="Adaptation")
sns.lineplot(data=results_aggregated, ax=ax9, x="Step", y="Savings")

sns.lineplot(data=unity_aggregated, ax=ax1, x="Step", y="Max Flood Inundation")
sns.lineplot(data=unity_aggregated, ax=ax2, x="Step", y="Income",label="Unity")
sns.lineplot(data=unity_aggregated, ax=ax3, x="Step", y="Nothing Utility")
sns.lineplot(data=unity_aggregated, ax=ax4, x="Step", y="Adapt Utility")
sns.lineplot(data=unity_aggregated, ax=ax5, x="Step", y="Migrate Utility")
sns.lineplot(data=unity_aggregated, ax=ax6, x="Step", y="Floods experienced")
sns.lineplot(data=unity_aggregated, ax=ax7, x="Step", y="Flood Damage")
sns.lineplot(data=unity_aggregated, ax=ax8, x="Step", y="Adaptation")
sns.lineplot(data=unity_aggregated, ax=ax9, x="Step", y="Savings")

# Add content to the subplots (optional)
ax1.set_ylabel('Max Inundation (m)')
ax2.set_ylabel('Income (k£)')
ax3.set_ylabel('Utility of Inaction')
ax4.set_ylabel('Utility of Adaptation')
ax5.set_ylabel('Utility of Migration')
ax6.set_ylabel('Floods experienced')
ax7.set_ylabel('Flood Damage (k£)')
ax8.set_ylabel('Defence Cost (k£)')
ax9.set_ylabel('Savings (k£)')

ax1.set_xlabel('Year')
ax2.set_xlabel('Year')
ax3.set_xlabel('Year')
ax4.set_xlabel('Year')
ax5.set_xlabel('Year')
ax6.set_xlabel('Year')
ax7.set_xlabel('Year')
ax8.set_xlabel('Year')
ax9.set_xlabel('Year')
# Add common titles above each row
rowtitle_size = 15

fig.text(0.97, 0.91, 'Inputs',va='center', ha='center', fontsize=rowtitle_size, rotation=-90)
fig.text(0.97, 0.67, 'Utility Calculations',va='center', ha='center', fontsize=rowtitle_size, rotation=-90)
fig.text(0.97, 0.3, 'Feedbacks',va='center', ha='center', fontsize=rowtitle_size, rotation=-90)


# Adjust layout to prevent overlapping
ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout(rect=[0, 0.05, 0.96, 1])
# Show the plot
plt.show()
# for row in range(5):

#     for col in range(2):      

#         index = int((col)+(2*row))
#         # print(index)

#         sns.lineplot(data=results_aggregated, ax=axes[row,col], x="Step", y=ys[index])


#         print("for index " + str(index) + " ys is " + ys[index] + " and its ylabel is " + ylabels[index] + " at position (" + str(row) + "," + str(col) + ")")

#         axes[row,col].set(
#             xlabel="Year",
#             ylabel=ylabels[index],
#         )

    
# plt.tight_layout()



# plt.savefig(f"..\\coastal_pngs\\plot_iter10_{timestamp}.png")


# Create a separate figure for the second plot
fig2 = plt.figure(figsize=(5, 3))  # Adjust the size as needed

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],  # Specify your preferred font here
})

sns.lineplot(data=results_aggregated, x="Step", y="Migration Count",label='Discounted')
sns.lineplot(data=unity_aggregated, x="Step", y="Migration Count",label='Unity')
plt.ylabel("Migration moves")
plt.xlabel("Year")
plt.legend()
# Your code for the second plot goes here

# Show the second plot
plt.show()