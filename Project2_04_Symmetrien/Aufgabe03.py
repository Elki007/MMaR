import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

einfach = mpimg.imread('CleanWindows.png')
mittel = mpimg.imread('CurvyWindows.png')


def plti(img):
    plt.imshow(img)
    plt.axis('off')
    plt.show()


plti(einfach)
plti(mittel)



#imgplot = plt.imshow(img)

#plt.show()