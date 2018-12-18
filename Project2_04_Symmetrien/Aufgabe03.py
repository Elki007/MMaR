import random, operator, imageio
import matplotlib.pylab as plt
import numpy as np
from datetime import datetime
from skimage.feature import hog
from skimage import data, exposure


einfach = imageio.imread('CleanWindows.png')
#einfach2 = misc.imread('CleanWindowsRed.png')
mittel = imageio.imread('CurvyWindows.png')
hard_t = imageio.imread('monge_true.png')
hard_s = imageio.imread('monge_simple.png')



def plti(img):
    plt.imshow(img)
    plt.axis('off')


def plot_patches(patches, best, amount, promt):
    fig = plt.figure(num='Symmetrieerkennung auf Bildern. ' + promt, figsize=(8, 2))  # Title and layout
    fig.subplots_adjust(wspace=0.3)     # adjust distance between subplots
    if len(best)> amount:
        columns = amount
    else:
        columns = len(best)
    rows = 1
    for i in range(1, columns * rows + 1):
        img = patches[best[i-1][1]].img
        #plt.axis('off')    # without axises it looks weird
        ax = fig.add_subplot(rows, columns, i)
        ax.title.set_text(str("Symm #: ") + str(patches[best[i-1][1]].count_symm))    # Title for subplot
        plt.imshow(img)
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
    print(f"x: {x} to {x+k}, y: {y} to {y+k}")
    return img[y:y + k, x:x + k]


def find_symmetry(source, patch, like):
    img = patch.img
    len = img.shape[0]
    ymax = source.shape[0]
    xmax = source.shape[1]
    for y in range(0, ymax-len):
        for x in range(0, xmax-len):
            A = crop(source, x, y, img)
            if np.array_equal(A, img):
                patch.add_symmetry()


def find_symmetry_2(source, patch, like):
    img = patch.img
    len = img.shape[0]
    ymax = source.shape[0]
    xmax = source.shape[1]

    for y in range(0, ymax-len):
        for x in range(0, xmax-len):
            A = crop(source, x, y, img)
            #A[0] #4 Stueck [255,255,255] [] [] []
            s = np.sum((A[:, :, 0:3] - img[:, :, 0:3]) ** 2)
            if s <= like:
                patch.add_symmetry()


def find_symmetry_HOG(A, B, like):
    """
    this function takes 2 images and makes two HOG images.
    :param A: first image (original)
    :param B: second image (simple image)
    :param like: no use
    :return: nothing, just plots an HOG image A and B
    :comment: by adjusting orientations = x, pixels_per_cell=(y, y),
    cells_per_block=(z, z) we may recieve better sample for further comparison
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

    fd_A, hog_image_A = hog(A, orientations=9, pixels_per_cell=(20, 20),
                    cells_per_block=(10, 10), visualize=True, multichannel=True)

    fd_B, hog_image_B = hog(B, orientations=8, pixels_per_cell=(16, 16),
                            cells_per_block=(1, 1), visualize=True, multichannel=True)

    # plotting

    ax1.axis('off')
    hog_image_rescaled_before = exposure.rescale_intensity(hog_image_A, in_range=(0, 10))
    ax1.imshow(hog_image_rescaled_before, cmap=plt.cm.gray)
    ax1.set_title('Image A')

    # Rescale histogram for better display
    hog_image_rescaled = exposure.rescale_intensity(hog_image_B, in_range=(0, 10))

    ax2.axis('off')
    ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
    ax2.set_title('Image B')
    plt.show()



def HOG(image):
    fd, hog_image = hog(image, orientations=16, pixels_per_cell=(16, 16),
                        cells_per_block=(1, 1), visualize=True, multichannel=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

    ax1.axis('off')
    hog_image_rescaled_before = exposure.rescale_intensity(hog_image, in_range=(0, 1))
    ax1.imshow(hog_image_rescaled_before, cmap=plt.cm.gray)
    ax1.set_title('Input image')

    # Rescale histogram for better display
    hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

    ax2.axis('off')
    ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
    ax2.set_title('Histogram of Oriented Gradients')
    plt.show()


def find_symmetry_3(source, patch, like):
    img = patch.img
    len = img.shape[0]
    ymax = source.shape[0]
    xmax = source.shape[1]


    f_ = np.mean(img[:, :, 0:3])
    #sigma_f = np.std(img, dtype=np.float64)
    for y in range(0, ymax-len):
        for x in range(0, xmax-len):
            A = crop(source, x, y, img)
            s = np.sum((A[:, :, 0:3] - img[:, :, 0:3]) ** 2)

            g_ = np.mean(A[:, :, 0:3])
            #sigma_g = np.std(A, dtype=np.float64)
            #print(f"g_:{g_}, sigma_g:{sigma_g}")
            #print(A[0][0])
            #print(np.sum(A[0][0]))
            s = 0
            for i in range(len):
                for j in range(len):
                    sigma_f = np.sqrt((np.mean(abs(np.sum(img[i][j]) - np.mean(img[i][j])) ** 2)))
                    sigma_g = np.sqrt((np.mean(abs(np.sum(A[i][j]) - np.mean(A[i][j])) ** 2)))
                    #print(f"f_:{f_}, sigma_f:{sigma_f}")
                    #print(f"g_:{g_}, sigma_g:{sigma_g}")
                    # why in some cases there is a "0" as sigma?
                    if sigma_f*sigma_g != 0:
                        s += ( (np.sum(img[i][j]) - f_)*(np.sum(A[i][j])-g_) )/(sigma_f*sigma_g)
            NCC = s/(len**2)
            #print(f"s:{s} NCC:{NCC}")
            if NCC <= like:
                patch.add_symmetry()


class Patch:
    def __init__(self, img):
        self.img = img
        self.count_symm = 0

    def __repr__(self):
        return self.img

    def add_symmetry(self):
        self.count_symm += 1

def test(image, time, k, promt, **kwargs):
    like = kwargs.get('like', 0)
    function = kwargs.get('function', 0)
    bound = kwargs.get('bound', False)
    if function == 0:
        return
    patches = []
    start = datetime.now()
    passed = 0
    best = []
    while passed < time:
        patches.append(Patch(crop_random(image, k)))
        function(image, patches[-1], like*k*k)  # Dynamic function (find_symmetry 1-3)
        end = datetime.now()
        passed = (end - start).seconds
        # best < bound ?
        best.append([patches[-1].count_symm, len(patches) - 1])
        # print("found symmetries #", patches[-1].count_symm)

    best.sort(key=operator.itemgetter(0), reverse=True)

    if bound:
        print(best)
        best = [a for a in best if (a[0] < bound)]
    print(best)

    plot_patches(patches, best, 5, promt)

########
##main##
########
#### Teil 1
time = 1    # second for algorithm
k = 12      # (size of a Patch)

#test(einfach, time, k, "Teil 1, einfach", function=find_symmetry, bound=1000)

time = 5
k = 32
#test(mittel, time, k, "Teil 1, mittel", function=find_symmetry, bound=1000)

#### Teil 2
time = 10   # second for algorithm
k = 32      # (size of a Patch)
like = 0    # SSD difference allowed
#test(einfach, time, k, "Teil 2, einfach", like=like, function=find_symmetry_2, bound=1000)

time = 10   # second for algorithm
k = 50      # (size of a Patch)
like = 70   # SSD difference allowed
#test(mittel, time, k, "Teil 2, mittel", like=like, function=find_symmetry_2, bound=100)

#### Teil 3
time = 10   # second for algorithm
k = 70      # (size of a Patch)
like = 70   # SSD difference allowed
find_symmetry_HOG(hard_t, hard_s, like)
#test(mittel, time, k, like=like, function=find_symmetry_HOG, bound=100000)