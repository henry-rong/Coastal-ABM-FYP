

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
from PIL import Image

# List of paths to your GeoTIFF files
# geotiff_files = sorted(glob("data/processed/rp0001/inuncoast_rcp8p5_nosub_*_rp0001_5_perc_05.tif.gz"))  # Add more files as needed
# geotiff_files = sorted(glob('data/windowed/**.gz'))
geotiff_files = sorted(glob('data/processed/rp0001/*.gz'))
# geotiff_files = sorted(glob('data/windowed/inuncoast_rcp8p5_nosub_*_rp0001_5_perc_05.tif.gz'))

# Set the desired frame size (in inches)
frame_width = 10
frame_height = 8

fig, ax = plt.subplots(figsize=(frame_width, frame_height))


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
# plt.show()

# Save each frame as an image
for i in range(len(geotiff_files)):
    update(i)  # Update the plot for each frame
    plt.savefig('frame_{}.png'.format(i), dpi=300)  # Save the current frame as a PNG image

# Combine the images into a GIF
images = []
for i in range(len(geotiff_files)):
    img = Image.open('frame_{}.png'.format(i))
    images.append(img)

images[0].save('animation.gif', save_all=True, append_images=images[1:], duration=1000, loop=0)