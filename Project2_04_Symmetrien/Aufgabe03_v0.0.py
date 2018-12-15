import numpy as np
from PIL import Image

image_clean_windows = Image.open("image/CleanWindows.png")
np_clean_windows = np.array(image_clean_windows.getdata())

print(image_clean_windows)
print(len(np_clean_windows))




