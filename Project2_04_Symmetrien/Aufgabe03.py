import numpy as np
import random, operator
import matplotlib.pylab as plt
import numpy as np
from datetime import datetime

einfach = plt.imread('CleanWindows.png')
mittel = plt.imread('CurvyWindows.png')


def plti(img):
    plt.imshow(img)
    plt.axis('off')
    plt.show()


def crop(img, startx, starty,second_img):
    y = img.shape[0]
    x = img.shape[1]
    k = second_img.shape[0]
    if starty + k > y or startx + k > x:
        return False
    return img[starty:starty + k, startx:startx + k]


def crop_random(img,k=8):
    y = img.shape[0]
    x = img.shape[1]
    x = random.randint(0, x - k)
    y = random.randint(0, y - k)
    return img[y:y + k, x:x + k]


def find_symmetry(source, patch):
    img = patch.img
    len = img.shape[0]
    ymax = source.shape[0]
    xmax = source.shape[1]
    for y in range(0, ymax-len):
        for x in range(0, xmax-len):
            A = crop(source, x, y, img)
            if np.array_equal(A, img):
                patch.add_symmetry()


class Patch:
    def __init__(self, img):
        self.img = img
        self.count_symm = 0

    def __repr__(self):
        return self.img

    def add_symmetry(self):
        self.count_symm += 1

########
##main##
########
time = 10   # second for algorithm
k = 20      # (size of a Patch)

patches = []
start = datetime.now()
passed = 0
best = []
while passed < time:
    patches.append(Patch(crop_random(einfach, k)))
    find_symmetry(einfach, patches[-1])
    end = datetime.now()
    passed = (end-start).seconds
    best.append([patches[-1].count_symm, len(patches)-1])
    #print("found symmetries #", patches[-1].count_symm)

print(best)
best.sort(key=operator.itemgetter(0), reverse=True)
print(best)

# show top 5 best patches
for i in range(5):
    #print(best[i][1])
    plti(patches[best[i][1]].img)