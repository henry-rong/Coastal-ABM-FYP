import rasterio
from glob import glob
import os
import gzip
import shutil
import numpy as np

# the following script loops through the filepaths

# raster1 = 'data/depth/inuncoast_historical_nosub_hist_rp0001_5_UK.tif.gz'

# with rasterio.open(f"/vsigzip/{raster1}") as r1:
        
#     data1 = r1.read(1)
    # print(r1.bounds)
    # BoundingBox(left=-10.008333333333326, bottom=49.875, right=1.7666666666666746, top=61.53333333333333)

###################################################


# Path to your gzipped GeoTIFF file
gzipped_geotiff_file = "data/windowed/inuncoast_rcp8p5_nosub_2030_rp0010_0_perc_05.tif.gz"

def open_gzipped_geotiff(filename):
    try:
        # Decompress the gzipped file
        with gzip.open(filename, 'rb') as f_in:
            # Create a temporary decompressed file
            with open("temp.tif", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Open the decompressed file with Rasterio
        dataset = rasterio.open("temp.tif")

        return dataset
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        # Clean up temporary file
        try:
            os.remove("temp.tif")
        except:
            pass


def calculate_difference(zip1, zip2, rp ,start_year,end_year):
    dest_path = f"data/processed/{rp}"  # destination path
    
    # Get the tail of the second zip file path
    tail = os.path.split(zip2)[1].split("_")

    # Open and read the GeoTIFF files
    d1 = open_gzipped_geotiff(zip1).read(1)
    d2 = open_gzipped_geotiff(zip2).read(1)
    
    if d1 is None or d2 is None:
        print("Error: Failed to open GeoTIFF files.")
        return
    
    # Calculate the difference between the datasets
    diff = d2 - d1
    
    # Calculate the difference per unit
    diff_unit = diff / (end_year - start_year)

    # d1_array = d1.read(1, masked=False)
    # d1_copy = np.copy(d1_array)


    for year in range(start_year, end_year+1):
        
        
        # Update the year in the tail
        temp_tail = tail.copy()
        temp_tail[3] = str(year)

        # Construct the output file path
        filepath = os.path.join(dest_path, "_".join(temp_tail))
        
        with rasterio.open("temp_difference.tif", 'w', **open_gzipped_geotiff(zip1).profile) as dst:
            dst.write(d1, 1)

        # Compress the temporary file using gzip
        with open("temp_difference.tif", 'rb') as f_in, gzip.open(filepath, 'wb') as f_out:
            f_out.writelines(f_in)

        # Remove the temporary file
        os.remove("temp_difference.tif")

        d1 += diff_unit

# r1 = "data/windowed/inuncoast_rcp8p5_nosub_2030_rp0001_5_perc_05.tif.gz"
# r2 = "data/windowed/inuncoast_rcp8p5_nosub_2050_rp0001_5_perc_05.tif.gz"

# # print(open_gzipped_geotiff(r2))

# calculate_difference(r1,r2,'rp0001',2030,2050)

##################################################

## mkdir rp0001 rp0002 rp0005 rp0010 rp0025 rp0050 rp0100 rp0250 rp0500 rp1000

# generate years from 2030 to 2080

# periods = [sorted(glob("data/windowed/inuncoast_rcp8p5_nosub_*_rp0001_5_perc_05.tif.gz")),
#         sorted(glob("data/windowed/inuncoast_rcp8p5_nosub_*_rp0002_0.tif.gz")),
#         sorted(glob("data/windowed/inuncoast_rcp8p5_nosub_*_rp0005_0.tif.gz")),
#         sorted(glob("data/windowed/inuncoast_rcp8p5_nosub_*_rp0010_0.tif.gz")),
#         sorted(glob("data/windowed/inuncoast_rcp8p5_nosub_*_rp0025_0.tif.gz")),
#         sorted(glob("data/windowed/inuncoast_rcp8p5_nosub_*_rp0050_0.tif.gz")),
#         sorted(glob("data/windowed/inuncoast_rcp8p5_nosub_*_rp0100_0.tif.gz")),
#         sorted(glob("data/windowed/inuncoast_rcp8p5_nosub_*_rp0250_0.tif.gz")),
#         sorted(glob("data/windowed/inuncoast_rcp8p5_nosub_*_rp0500_0.tif.gz")),
#         sorted(glob("data/windowed/inuncoast_rcp8p5_nosub_*_rp1000_0.tif.gz"))]


# rps = ['rp0001', 'rp0002', 'rp0005', 'rp0010', 'rp0025', 'rp0050', 'rp0100', 'rp0250', 'rp0500', 'rp1000']
# years = [2030,2050,2080]

# for rp in range(len(rps)):

#     period = periods[rp]

#     for y in range(len(period)-1):
#         calculate_difference(period[y],period[y+1],rps[rp],years[y],years[y+1])


## --> generate years from 2010 (baseline) to 2030 for rp1000

# periods = [sorted(glob("data/windowed/inuncoast_historical_nosub_hist_rp0001_5.tif.gz")), sorted(glob("data/windowed/inuncoast_rcp8p5_nosub_2030_rp0001_5_perc_05.tif.gz"))]

# calculate_difference(periods[0][0],periods[1][0],'rp0001',2010,2030)

# print(periods)

## --> genrate years from 2010 (baseline) to 2030 for other rp

rps = ['rp0002', 'rp0005', 'rp0010', 'rp0025','rp0050', 'rp0100', 'rp0250', 'rp0500', 'rp1000']

years = [2010,2030]

periods = [sorted(glob("data/windowed/inuncoast_historical_nosub_hist_*_0.tif.gz")), sorted(glob("data/windowed/inuncoast_rcp8p5_nosub_2030_*_0.tif.gz"))]


for rp in range(len(rps)):
    calculate_difference(periods[0][rp],periods[1][rp],rps[rp],years[0],years[1])