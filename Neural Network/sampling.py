#!/usr/bin/python

from skimage.transform import pyramid_gaussian
import cv2


# load the image
image = cv2.imread("../data/images/tile3_25.pgm")
            

# METHOD #2: Resizing + Gaussian smoothing.
for (i, resized) in enumerate(pyramid_gaussian(image, downscale=1.5)):
	# if the image is too small, break from the loop
	if resized.shape[0] < 30 or resized.shape[1] < 30:
		break
		
	# show the resized image
	cv2.imshow("Layer {}".format(i + 1), resized)
	cv2.waitKey(0)
