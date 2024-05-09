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
# unity_results = pd.read_csv(f"..\\coastal_csvs\\results_unit_discount_2024-05-08_21-50-07.csv")

results_filtered = results_df
results_filtered.drop(columns=['AgentID','RunId'], inplace=True)
# unity_filtered = unity_results
# unity_filtered.drop(columns=['AgentID','RunId','data_label'], inplace=True)

# unity_aggregated = unity_filtered.groupby(["iteration","Step"]).mean().reset_index()
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
ax3 = fig.add_subplot(gs[0, 0:2])   # Second row, first column
ax4 = fig.add_subplot(gs[0, 2:4])   # Second row, second column
ax5 = fig.add_subplot(gs[0, 4:6])   # Second row, third column
ax6 = fig.add_subplot(gs[1, 1:3])   
ax7 = fig.add_subplot(gs[1, 3:5])   
ax8 = fig.add_subplot(gs[2, 1:3])  
ax9 = fig.add_subplot(gs[2, 3:5])  
ax10 = fig.add_subplot(gs[3, 2:4])

# Seaborn plots
sns.lineplot(data=results_aggregated, ax=ax3, x="Step", y="Nothing Utility")
sns.lineplot(data=results_aggregated, ax=ax4, x="Step", y="Adapt Utility")
sns.lineplot(data=results_aggregated, ax=ax5, x="Step", y="Migrate Utility")
sns.lineplot(data=results_aggregated, ax=ax6, x="Step", y="Floods experienced")
sns.lineplot(data=results_aggregated, ax=ax7, x="Step", y="Flood Damage")
sns.lineplot(data=results_aggregated, ax=ax8, x="Step", y="Adaptation")
sns.lineplot(data=results_aggregated, ax=ax9, x="Step", y="Savings")
sns.lineplot(data=results_aggregated, ax=ax10, x="Step", y="Migration Count")

# data for neighbours
# migration_results_df = pd.read_csv(f"..\\coastal_csvs\\migration_results_neighbourhood_radius_2024-05-08_04-15-56.csv")
# adaptation_results_df = pd.read_csv(f"..\\coastal_csvs\\adaptation_results_neighbourhood_radius_2024-05-08_04-15-56.csv")
# flood_dmg_results_df = pd.read_csv(f"..\\coastal_csvs\\damage_results_neighbourhood_radius_2024-05-08_04-15-56.csv")
# flood_exp_results_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_neighbourhood_radius_2024-05-08_04-15-56.csv")
# utility_nothing_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_nothing_results_neighbourhood_radius_2024-05-08_04-15-56.csv")
# utility_adapt_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_adapt_results_neighbourhood_radius_2024-05-08_04-15-56.csv")
# utility_migrate_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_migrate_results_neighbourhood_radius_2024-05-08_04-15-56.csv")
# saving_results_df = pd.read_csv(f"..\\coastal_csvs\\savings_results_neighbourhood_radius_2024-05-08_04-15-56.csv")

# migration_results_df = pd.read_csv(f"..\\coastal_csvs\\migration_results_initial_flood_experience_2024-05-08_06-01-32.csv")
# adaptation_results_df = pd.read_csv(f"..\\coastal_csvs\\adaptation_results_initial_flood_experience_2024-05-08_06-01-32.csv")
# flood_dmg_results_df = pd.read_csv(f"..\\coastal_csvs\\damage_results_initial_flood_experience_2024-05-08_06-01-32.csv")
# flood_exp_results_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_initial_flood_experience_2024-05-08_06-01-32.csv")
# utility_nothing_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_nothing_results_initial_flood_experience_2024-05-08_06-01-32.csv")
# utility_adapt_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_adapt_results_initial_flood_experience_2024-05-08_06-01-32.csv")
# utility_migrate_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_migrate_results_initial_flood_experience_2024-05-08_06-01-32.csv")
# saving_results_df = pd.read_csv(f"..\\coastal_csvs\\savings_results_initial_flood_experience_2024-05-08_06-01-32.csv")

# hue_val = "initial_flood_experience"
# migration_results_df = pd.read_csv(f"..\\coastal_csvs\\migration_results_initial_flood_preparedness_2024-05-08_04-30-57.csv")
# adaptation_results_df = pd.read_csv(f"..\\coastal_csvs\\adaptation_results_initial_flood_preparedness_2024-05-08_04-30-57.csv")
# flood_dmg_results_df = pd.read_csv(f"..\\coastal_csvs\\damage_results_initial_flood_preparedness_2024-05-08_04-30-57.csv")
# flood_exp_results_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_initial_flood_preparedness_2024-05-08_04-30-57.csv")
# utility_nothing_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_nothing_results_initial_flood_preparedness_2024-05-08_04-30-57.csv")
# utility_adapt_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_adapt_results_initial_flood_preparedness_2024-05-08_04-30-57.csv")
# utility_migrate_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_migrate_results_initial_flood_preparedness_2024-05-08_04-30-57.csv")
# saving_results_df = pd.read_csv(f"..\\coastal_csvs\\savings_results_initial_flood_preparedness_2024-05-08_04-30-57.csv")

# hue_val = "initial_flood_preparedness"
# migration_results_df = pd.read_csv(f"..\\coastal_csvs\\migration_results_house_sample_size_2024-05-08_04-31-36.csv")
# adaptation_results_df = pd.read_csv(f"..\\coastal_csvs\\adaptation_results_house_sample_size_2024-05-08_04-31-36.csv")
# flood_dmg_results_df = pd.read_csv(f"..\\coastal_csvs\\damage_results_house_sample_size_2024-05-08_04-31-36.csv")
# flood_exp_results_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_house_sample_size_2024-05-08_04-31-36.csv")
# utility_nothing_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_nothing_results_house_sample_size_2024-05-08_04-31-36.csv")
# utility_adapt_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_adapt_results_house_sample_size_2024-05-08_04-31-36.csv")
# utility_migrate_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_migrate_results_house_sample_size_2024-05-08_04-31-36.csv")
# saving_results_df = pd.read_csv(f"..\\coastal_csvs\\savings_results_house_sample_size_2024-05-08_04-31-36.csv")

# hue_val = "house_sample_size"
# migration_results_df = pd.read_csv(f"..\\coastal_csvs\\migration_results_savings_mean_2024-05-08_04-31-29.csv")
# adaptation_results_df = pd.read_csv(f"..\\coastal_csvs\\adaptation_results_savings_mean_2024-05-08_04-31-29.csv")
# flood_dmg_results_df = pd.read_csv(f"..\\coastal_csvs\\damage_results_savings_mean_2024-05-08_04-31-29.csv")
# flood_exp_results_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_savings_mean_2024-05-08_04-31-29.csv")
# utility_nothing_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_nothing_results_savings_mean_2024-05-08_04-31-29.csv")
# utility_adapt_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_adapt_results_savings_mean_2024-05-08_04-31-29.csv")
# utility_migrate_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_migrate_results_savings_mean_2024-05-08_04-31-29.csv")
# saving_results_df = pd.read_csv(f"..\\coastal_csvs\\savings_results_savings_mean_2024-05-08_04-31-29.csv")

# hue_val = "savings_mean"
# migration_results_df = pd.read_csv(f"..\\coastal_csvs\\migration_results_income_mean_2024-05-08_13-55-18.csv")
# adaptation_results_df = pd.read_csv(f"..\\coastal_csvs\\adaptation_results_income_mean_2024-05-08_13-55-18.csv")
# flood_dmg_results_df = pd.read_csv(f"..\\coastal_csvs\\damage_results_income_mean_2024-05-08_13-55-18.csv")
# flood_exp_results_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_income_mean_2024-05-08_13-55-18.csv")
# utility_nothing_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_nothing_results_income_mean_2024-05-08_13-55-18.csv")
# utility_adapt_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_adapt_results_income_mean_2024-05-08_13-55-18.csv")
# utility_migrate_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_migrate_results_income_mean_2024-05-08_13-55-18.csv")
# saving_results_df = pd.read_csv(f"..\\coastal_csvs\\savings_results_income_mean_2024-05-08_13-55-18.csv")

# hue_val = "income_mean"

# migration_results_df = pd.read_csv(f"..\\coastal_csvs\\migration_results_fixed_migration_cost_2024-05-08_04-28-45.csv")
# adaptation_results_df = pd.read_csv(f"..\\coastal_csvs\\adaptation_results_fixed_migration_cost_2024-05-08_04-28-45.csv")
# flood_dmg_results_df = pd.read_csv(f"..\\coastal_csvs\\damage_results_fixed_migration_cost_2024-05-08_04-28-45.csv")
# flood_exp_results_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_fixed_migration_cost_2024-05-08_04-28-45.csv")
# utility_nothing_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_nothing_results_fixed_migration_cost_2024-05-08_04-28-45.csv")
# utility_adapt_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_adapt_results_fixed_migration_cost_2024-05-08_04-28-45.csv")
# utility_migrate_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_migrate_results_fixed_migration_cost_2024-05-08_04-28-45.csv")
# saving_results_df = pd.read_csv(f"..\\coastal_csvs\\savings_results_fixed_migration_cost_2024-05-08_04-28-45.csv")

# hue_val = "fixed_migration_cost"
migration_results_df = pd.read_csv(f"..\\coastal_csvs\\migration_results_variable_migration_cost_2024-05-08_04-28-28.csv")
adaptation_results_df = pd.read_csv(f"..\\coastal_csvs\\adaptation_results_variable_migration_cost_2024-05-08_04-28-28.csv")
flood_dmg_results_df = pd.read_csv(f"..\\coastal_csvs\\damage_results_variable_migration_cost_2024-05-08_04-28-28.csv")
flood_exp_results_df = pd.read_csv(f"..\\coastal_csvs\\exp_results_variable_migration_cost_2024-05-08_04-28-28.csv")
utility_nothing_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_nothing_results_variable_migration_cost_2024-05-08_04-28-28.csv")
utility_adapt_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_adapt_results_variable_migration_cost_2024-05-08_04-28-28.csv")
utility_migrate_results_df = pd.read_csv(f"..\\coastal_csvs\\utility_migrate_results_variable_migration_cost_2024-05-08_04-28-28.csv")
saving_results_df = pd.read_csv(f"..\\coastal_csvs\\savings_results_variable_migration_cost_2024-05-08_04-28-28.csv")

hue_val = "variable_migration_cost"

sns.lineplot(data=utility_nothing_results_df, ax=ax3, x="Step", y="Nothing Utility", hue = hue_val, markers=['o', 'x','+'],legend=False,palette="colorblind")
sns.lineplot(data=utility_adapt_results_df, ax=ax4, x="Step", y="Adapt Utility", hue = hue_val, markers=['o', 'x','+'],legend=False,palette="colorblind")
sns.lineplot(data=utility_migrate_results_df, ax=ax5, x="Step", y="Migrate Utility", hue = hue_val, markers=['o', 'x','+'],legend=False,palette="colorblind")
sns.lineplot(data=flood_exp_results_df, ax=ax6, x="Step", y="Floods experienced", hue = hue_val, markers=['o', 'x','+'], legend=False,palette="colorblind")
sns.lineplot(data=flood_dmg_results_df, ax=ax7, x="Step", y="Flood Damage", hue = hue_val, markers=['o', 'x','+'],legend=False,palette="colorblind")
sns.lineplot(data=adaptation_results_df, ax=ax8, x="Step", y="Adaptation", hue = hue_val, markers=['o', 'x','+'], legend=False,palette="colorblind")
sns.lineplot(data=saving_results_df, ax=ax9, x="Step", y="Savings", hue = hue_val, markers=['o', 'x','+'], legend=False,palette="colorblind")
sns.lineplot(data=migration_results_df, ax=ax10, x="Step", y="Migration Count", hue = hue_val, markers=['o', 'x','+'],palette="colorblind")

# Add content to the subplots (optional)
ax3.set_ylabel('Utility of Inaction')
ax4.set_ylabel('Utility of Adaptation')
ax5.set_ylabel('Utility of Migration')
ax6.set_ylabel('Floods experienced')
ax7.set_ylabel('Flood Damage (k£)')
ax8.set_ylabel('Defence Cost (k£)')
ax9.set_ylabel('Savings (k£)')
ax10.set_ylabel('Migration moves')

ax3.set_xlabel('Year')
ax4.set_xlabel('Year')
ax5.set_xlabel('Year')
ax6.set_xlabel('Year')
ax7.set_xlabel('Year')
ax8.set_xlabel('Year')
ax9.set_xlabel('Year')
ax10.set_xlabel('Year')
# Add common titles above each row
rowtitle_size = 15

fig.text(0.97, 0.89, 'Utility Calculations',va='center', ha='center', fontsize=rowtitle_size, rotation=-90)
fig.text(0.97, 0.49, 'Feedbacks',va='center', ha='center', fontsize=rowtitle_size, rotation=-90)
fig.text(0.97, 0.2, 'Output',va='center', ha='center', fontsize=rowtitle_size, rotation=-90)


# Adjust layout to prevent overlapping
ax10.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout(rect=[0, 0.05, 0.96, 1])
# Show the plot
plt.show()