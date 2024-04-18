import rasterio
import numpy as np
from rasterio.plot import show
from rasterio.mask import mask
from matplotlib import pyplot
import geopandas as gpd
from glob import glob
import os
import gzip

# get shapefile defining extent to window (clip) raster file

world_zip_file = 'data/clip2.zip'

shapes = gpd.GeoDataFrame.from_file(world_zip_file).geometry

# east, south, west, north  = gpd.GeoDataFrame.from_file(world_zip_file).total_bounds

# world_bounds = rasterio.coords.BoundingBox(west, south, east, north)

dest_path = 'data/windowed/' # destination path

# files = glob('data/preprocess/2080/inuncoast_rcp8p5_nosub_2080_rp0002_0_perc_50.tif')
# files = sorted(glob('data/preprocess/**/*.tif'))
files = ["data/preprocess/2030/inuncoast_rcp8p5_nosub_2030_rp0001_5.tif"]
for file in files:
    
    tail = os.path.split(file)[1]
    
    # crop each global file to UK and gzip

    with rasterio.open(file) as r:

        out_image, out_transform = mask(r,shapes,crop=True)

        out_meta = r.meta
        
        out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})
        
        with rasterio.open(dest_path + tail,"w",**out_meta) as dest:
            dest.write(out_image)

    # gzip the created file
    # f_in = open(dest_path + tail)
    # f_out = gzip.open(dest_path + tail + '.gz','wb')
    # f_out.writelines(f_in)
    # f_in.close()
    # f_out.close()
    # os.remove(dest_path + tail)

    # pyplot.imshow(out_image.T, cmap='pink')
    # pyplot.show()
    
###################################################




