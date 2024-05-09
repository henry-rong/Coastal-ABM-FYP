import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from datetime import datetime



# data

migration_results_df = []
flood_results_df = []
adaptation_results_df = []
flood_dmg_results_df = []
flood_exp_results_df = []
utility_nothing_results_df = []
utility_adapt_results_df = []
utility_migrate_results_df = []
saving_results_df = []
income_results_df = []

# labels

ylabels = ["Migration Count (moves)", "Max Flood Inundation (m)", "Average flood defence height (m)","Average damage (k£)","Number of households experiencing flooding","Utility of nothing","Utility of adapt","Utility of migration","Savings"]
# titles = ["Migration Count from 2010 to 2080", "Max Flood Inundation Rise from 2010 to 2080", "Flood Adaptation Change from 2010 to 2080","Average flood depth damage per year from 2010 to 2080","Average flood experience count per year from 2010 to 2080","Utility of nothing","Utility of adapt","Utility of migration","Savings"]
ys = ["Migration Count", "Max Flood Inundation", "Adaptation","Flood Damage","Floods experienced","Nothing Utility","Adapt Utility","Migrate Utility","Savings"]
data_sources = [migration_results_df, flood_results_df, adaptation_results_df,flood_dmg_results_df,flood_exp_results_df,utility_nothing_results_df,utility_adapt_results_df,utility_migrate_results_df,saving_results_df,income_results_df]

# parameters of sensitivity analysis
hues = ["neighbourhood_radius","initial_flood_experience","initial_flood_preparedness","house_sample_size","savings_mean","income_mean","fixed_migration_cost","variable_migration_cost"]

# create a figure for all 8 hue values, subplotting each ys

