import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plt_image(img):
    plt.imshow(img)
    #plt.axis('off')
    plt.show()


def crop_patch(np_img, x, y, length):
    pass


if __name__ == "__main__":
    image_clean_windows = plt.imread("image/CleanWindows.png")

    print(len(image_clean_windows))  # y
    print(len(image_clean_windows[0]))  # x

    print()

    print(image_clean_windows[0, 1])

    fig, ax = plt.subplots()

    print("fig:", fig)
    print("ax:", ax)

    #print(newer_img)

    patch = patches.Rectangle((50, 50), 100, 100)

    #image_clean_windows.set_clip_path(patch)

    #np_new_image = np.array(patch)

    #print(np_new_image)

    #plt.show()

    #print(new_img)

    #print(np_clean_windows[0][0])

    #print(np_clean_windows[0][0] == np_clean_windows[0][1])

    #print(list(np_clean_windows[0][0]))
    #print(np_clean_windows[0][1])

    #for row in np_clean_windows:
    #    for each in row:
    #        if not np.array_equal(each, np_clean_windows[0][0]):
    #            print(each)

    #print(np_clean_windows)

    #plt_image(image_clean_windows)


