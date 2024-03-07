from PIL import Image
import numpy as np
from scipy.ndimage import zoom
im = Image.open("simple_coast.png")
# print(im.format, im.size, im.mode)

gray = im.convert('L')
bw = gray.point(lambda x: 0 if x<128 else 255, '1')  #binarization
bw_array = np.array(bw)
bw_array_zoom = zoom(bw_array, 1/6)
np.savetxt('bw.txt', bw_array_zoom, fmt="%d")