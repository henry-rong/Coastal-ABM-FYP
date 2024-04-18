

##################################### invalid file checker

import os
import glob
import gzip
import shutil
import rasterio

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

def find_invalid_files(directory):
    invalid_files = []
    
    # Get a list of all compressed GeoTIFF files in the directory
    files = glob.glob(os.path.join(directory, "*.tif.gz"))
    
    for file in files:
        # Attempt to open the compressed GeoTIFF file
        dataset = open_gzipped_geotiff(file)
        
        # Check if the dataset is invalid (None)
        if dataset is None:
            invalid_files.append(file)
    
    return invalid_files

# Test the function with a directory containing compressed GeoTIFF files
directory_path = "data/processed/rp0001"
invalid_files = find_invalid_files(directory_path)

if invalid_files:
    print("Invalid files found:")
    for file in invalid_files:
        print(file)
else:
    print("No invalid files found.")