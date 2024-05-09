from coastal_model.model import CoastalModel
import mesa

params = {
    "data_label":"test",
    "neighbourhood_radius": 50,
    "initial_flood_experience": 0,
    "initial_flood_preparedness": 4, # the return period protection standard at 2010, ranging with all 9 
    "house_sample_size": 3,
    "savings_mean": 40,
    "income_mean": 30,
    "fixed_migration_cost": 5, #k£
    "variable_migration_cost": 0.001 #k£ per m
}

results = mesa.batch_run(
    CoastalModel,
    parameters=params,
    iterations=1,
    max_steps=69,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)
