import cv2 as cv
import os
from sys import platform
import numpy as np


def preprocess(image_size=200, contrast=0, brightness=1):
    """Parameter 'image_size' sets the length and width of the image.
    This method takes the imput. """
    WHITE = [255, 255, 255]
    SIZE = image_size

    # You shouldn't need to change this variable so long as you've got
    # your source code in the original src folder. If you do, please comment
    # it here.
    rootdir = '../data/images/'

    # a check to see which platform you're using. These commands will
    # delete your existing normalized images before create a new set.
    if (platform == "darwin" or platform == "linux" or platform == "linux2"):
        cmd1 = ("rm " + rootdir + "normalized_images/crater/*.jpg")
        cmd2 = ("rm " + rootdir + "normalized_images/non-crater/*.jpg")
        os.system(cmd1)
        os.system(cmd2)
    elif (platform == "win32" or platform == "cygwin"):
        cmd1 = ("del /f " + rootdir + "normalized_images/crater/*.jpg")
        cmd2 = ("del /f " + rootdir + "normalized_images/non-crater/*.jpg")
        os.system(cmd1)
        os.system(cmd2)

    for root, dirs, files in os.walk(rootdir + 'tile3_24/'):

        # Skip hidden directories and files.
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files[:] = [f for f in files if not f.startswith('.')]

        for file in files:
            img = cv.imread(rootdir + 'tile3_24/' +
                            os.path.basename(root) + '/' + file)
            dims = img.shape

            if(contrast > 0):
                # contrast control
                img = (img - 0.5) * contrast + (0.5 * brightness)
                '''
                # brightness control, not working yet. Overflow error.
                beta_img = cv.add(alpha_img, np.array([beta]))
                training_data.append(
                    (np.reshape(np.array(beta_img) / 255,
                                (len(np.array(beta_img))**2, 1)), label, file))
                '''

            # Check if source image does not match image_size argument.
            if(dims[0] > SIZE or dims[1] > SIZE or (dims[0] < SIZE and dims[1] < SIZE)):

                # Scale while maintaining aspect ratio.
                if(dims[0] > dims[1]):
                    ratio = float(SIZE) / float(dims[0])
                    newdim = (SIZE, int(dims[1] * ratio))
                else:
                    ratio = float(SIZE) / (dims[1])
                    newdim = (int(dims[0] * ratio), SIZE)

                img2 = cv.resize(img, (newdim[0], newdim[1]), interpolation=cv.INTER_CUBIC)
                #img2 = cv.resize(img, (image_size, image_size), interpolation=cv.INTER_CUBIC)
                img = img2
                dims = img.shape

            y1 = (SIZE - dims[0] + 1) // 2  # add 1 to round up if odd
            y2 = (SIZE - dims[0] + 0) // 2  # this one will round down
            x1 = (SIZE - dims[1] + 1) // 2  # "//" = integer division
            x2 = (SIZE - dims[1] + 0) // 2

            output_image = (cv.copyMakeBorder(img, y1, y2, x1,
                                              x2, cv.BORDER_CONSTANT, value=WHITE))
            #constant = cv.copyMakeBorder(output_image,padding,padding,padding,padding,cv.BORDER_CONSTANT,value=WHITE)
            cv.imwrite((rootdir + 'normalized_images/' +
                        os.path.basename(root) + '/' + file), output_image)
# preprocess(100)
