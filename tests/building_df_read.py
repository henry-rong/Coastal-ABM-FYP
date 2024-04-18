import geopandas as gpd

buildings_file = "data/fairbourne_buildings.geojson"

buildings_df = gpd.read_file(buildings_file)

# print(buildings_df.columns.values)
print(buildings_df.geometry.to_crs("EPSG:27700").area)