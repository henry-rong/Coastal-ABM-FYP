from coastal_model.model import CoastalModel
import mesa

params = {
    "people_per_household": 3.5,
    "neighbourhood_radius": 50,
    "initial_flood_experience": 0,
    "initial_flood_preparedness": 3, # the return period protection standard at 2010, ranging with all 9 
    "house_sample_size": 3,
    "fixed_migration_cost": 5, #k£
    "household_adaptation_cost": 10 #k£
}

results = mesa.batch_run(
    CoastalModel,
    parameters=params,
    iterations=1,
    max_steps=1,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)
