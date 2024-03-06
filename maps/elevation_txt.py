from PIL import Image
import numpy as np
from scipy.ndimage import zoom
im = Image.open("coast_with_elevation.png")
# print(im.format, im.size, im.mode)

gray = im.convert('L')
hist = gray.histogram()
values = set(hist)
bw = gray.point(lambda x: 0 if x>240 else (1 if x > 190 else (2 if x > 140 else 3)))
bw_array = np.array(bw)
bw_array_zoom = zoom(bw_array, 1/6)
np.savetxt('levels.txt', bw_array_zoom, fmt="%d")