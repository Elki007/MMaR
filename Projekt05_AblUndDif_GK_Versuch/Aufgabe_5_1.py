"""
Install pillow to import PIL:
Beside installing numpy and matplotlib you have to install pillow to be able to import PIL
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image

# Bild einlesen (bild.png ist im selben verzeichnis, wie diese Datei enthalten)
# convert("L") übersetzt das bild in ein Graustufenbild (nur ein Kanal, statt dreien)
image = Image.open("Katze.png").convert("L")

# konvertieren in ein numpy-array
img = np.asarray(image)

print(img)

img.flags.writeable = True

width = len(img[0])
height = len(img)
h = 1

abl_nach_x = []
abl_nach_y = []

for y in range(height):
    new_nach_x = []
    new_nach_y = []

    for x in range(width):
        if x >= h and x < width-h:
            new_nach_x.append((img[y][x + h] // 2 - img[y][x - h] // 2))
        else:
            new_nach_x.append(0)

        if y >= h and y < height-h:
            new_nach_y.append((img[y + h][x] // 2 - img[y - h][x] // 2))

    abl_nach_x.append(new_nach_x)
    abl_nach_y.append(new_nach_y) if len(new_nach_y) > 0 else abl_nach_y.append([0] * width)


abl_laenge = []

for y in range(height):
    new_nach_laenge = []

    for x in range(width):
        new_nach_laenge.append(int(math.sqrt(abl_nach_x[y][x]**2 + abl_nach_y[y][x]**2)))

    abl_laenge.append(new_nach_laenge)


# Anzeigen (in Graustufen)
"""
fig, ax = plt.subplots()
ax.imshow(abl_laenge, cmap='gray')
"""

fig = plt.figure()
bild_normal_obenlinks = fig.add_subplot(221)
bild_x_abl_obenrechts = fig.add_subplot(222)
bild_y_abl_untenlinks = fig.add_subplot(223)
bild_richtung_untenrechts = fig.add_subplot(224)

bild_normal_obenlinks.imshow(img, cmap='gray')
bild_x_abl_obenrechts.imshow(abl_nach_x, cmap='gray')
bild_y_abl_untenlinks.imshow(abl_nach_y, cmap='gray')
bild_richtung_untenrechts.imshow(abl_laenge, cmap='gray')

plt.show()
