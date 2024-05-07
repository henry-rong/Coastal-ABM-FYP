import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from coastal_model.model import CoastalModel
import os
from mesa.batchrunner import batch_run
from multiprocessing import freeze_support, Pool

current_directory = os.getcwd()
os.chdir(current_directory)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

no_of_neighbours = 0

csv_file_path = f"..\\coastal_csvs\\results_{no_of_neighbours}_{timestamp}.csv"

params = {
    "neighbourhood_radius": 50,
    "initial_flood_experience": 0,
    "initial_flood_preparedness": 4, # the return period protection standard at 2010, ranging with all 9 
    "house_sample_size": 3,
    "savings_mean": 40,
    "income_mean": 30,
    "fixed_migration_cost": 5, #k£
}
# params = {
#     "neighbourhood_radius": range(0,75,25),
#     "initial_flood_experience": range(2),
#     "initial_flood_preparedness": range(4), # the return period protection standard at 2010, ranging with all 9 
#     "house_sample_size": range(1,4),
#     "savings_mean": range(25,100,25),
#     "income_mean": range(20,50,10),
#     "fixed_migration_cost": range(5,15,5), #k£
# }

if __name__ == '__main__':
    freeze_support()
    results = batch_run(
    CoastalModel,
    parameters=params,
    iterations=2,
    max_steps=69,
    number_processes=None,
    data_collection_period=1,
    display_progress=True,
    )