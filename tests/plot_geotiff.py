

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

from glob import glob
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import rasterio
from rasterio.plot import show
import gzip
import shutil
import os
import matplotlib.colors as colors

# List of paths to your GeoTIFF files
# geotiff_files = sorted(glob("data/processed/rp0001/inuncoast_rcp8p5_nosub_*_rp0001_5_perc_05.tif.gz"))  # Add more files as needed
# geotiff_files = sorted(glob('data/windowed/**.gz'))
geotiff_files = sorted(glob('data/processed/rp0001/*.gz'))
# geotiff_files = sorted(glob('data/windowed/inuncoast_rcp8p5_nosub_*_rp0001_5_perc_05.tif.gz'))


fig, ax = plt.subplots()

def update(frame):
    ax.clear()
    file_name = os.path.basename(geotiff_files[frame])
    file_name_without_extension = os.path.splitext(file_name)[0]
    with open_gzipped_geotiff(geotiff_files[frame]) as src:
        data = src.read(1)  # Assuming single-band raster
        show(data, ax=ax, cmap='seismic', norm=colors.SymLogNorm(linthresh=0.03, linscale=0.03, vmin=data.min(), vmax=data.max()))  
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                ax.text(j, i, '{:.3f}'.format(data[i, j]), ha='center', va='center', color='white')  # Add text annotations with heatmap values
    ax.set_title(file_name_without_extension)
    ax.set_axis_off()

ani = animation.FuncAnimation(fig, update, frames=len(geotiff_files), interval=100)
plt.show()