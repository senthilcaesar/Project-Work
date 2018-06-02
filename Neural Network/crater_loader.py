import os
import numpy as np
import cv2 as cv
# from PIL import Image


def load_crater_data_wrapper(rotate=0):
    """This method takes the normalizd images, splits them into training data
    or test data (validation data in the future??) while formatting it for
    input into the network."""
    rootdir = '../data/images/normalized_images/'
    training_data = []
    validation_data = []
    test_data = []

    for root, dirs, files in os.walk(rootdir):
        # Skip hidden directories and files.
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files[:] = [f for f in files if not f.startswith('.')]

        for f in files:
            img = cv.imread(rootdir + os.path.basename(root) + '/' + f, 0)
            label = -1
            (h, w) = img.shape[:2]
            center = (w / 2, h / 2)
            degree = 0
            if os.path.basename(root) == 'crater':
                label = 1
            elif os.path.basename(root) == 'non-crater':
                label = 0
            if label != -1:  # just in case
                if np.random.rand() <= 0.7:
                    training_data.append(
                        (np.reshape(np.array(img) / 255,
                                    (len(np.array(img))**2, 1)), label, f))

                    if rotate == 1:
                        # Rotated img by 90
                        degree += 90
                        m = cv.getRotationMatrix2D(center, degree, 1)
                        rotated = cv.warpAffine(img, m, (w, h))
                        training_data.append(
                            (np.reshape(np.array(rotated) / 255,
                                        (len(np.array(rotated))**2, 1)), label, f))
                        # Rotated img by 180
                        degree += 90
                        m = cv.getRotationMatrix2D(center, degree, 1)
                        rotated = cv.warpAffine(img, m, (w, h))
                        training_data.append(
                            (np.reshape(np.array(rotated) / 255,
                                        (len(np.array(rotated))**2, 1)), label, f))
                        # Rotated img by 270
                        degree += 90
                        m = cv.getRotationMatrix2D(center, degree, 1)
                        rotated = cv.warpAffine(img, m, (w, h))
                        training_data.append(
                            (np.reshape(np.array(rotated) / 255,
                                        (len(np.array(rotated))**2, 1)), label, f))
                else:
                    test_data.append(
                        (np.reshape(np.array(img) / 255,
                                    (len(np.array(img))**2, 1)), label, f))

    return training_data, validation_data, test_data


def load_crater_data_phaseII_wrapper(contrast = 0, brightness = 1, rotate=1):
    """This method takes the normalized images, splits them into
    training data or test data (validation data in the future??)
    while formatting it for input into the network."""
    rootdir = '../data/images/normalized_images/'
    training_data = []
    test_data = []
    valid_data = []
    train_label = []
    test_label = []
    valid_label = []

    for root, dirs, files in os.walk(rootdir):
        # Skip hidden directories and files.
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files[:] = [f for f in files if not f.startswith('.')]

        for f in files:
            img = cv.imread(rootdir + os.path.basename(root) + '/' + f, 0)
            label = -1

            if os.path.basename(root) == 'crater':
                label = 1
            elif os.path.basename(root) == 'non-crater':
                label = 0
            
            if label != -1:  # just in case
                if contrast > 0:
                    img = (img - 0.5) * contrast + 0.5
                if brightness != 1:
                    img = img - 0.5 + (brightness * 0.5)
                training_data.append(img.flatten()/float(255))
                train_label.append(label)

                #if rotate == 1:
                        # rotate by 90 degrees
                      #imgr = np.rot90(img, 1)
                      #training_data.append(imgr.flatten()/float(255))
                      #train_label.append(label)

                      # rotate by 180 degrees
                      #imgr = np.rot90(img, 2)
                      #training_data.append(imgr.flatten() / float(255))
                      #train_label.append(label)

                        # rotate by 270 degrees
                        #imgr = np.rot90(img, 3)
                        #training_data.append(imgr.flatten() / float(255))
                        #train_label.append(label)






    tr_d = np.array(training_data)
    tr_l = np.array(train_label)
    randomize = np.arange(len(tr_d))
    np.random.shuffle(randomize)
    tr_d = tr_d[randomize]
    tr_l = tr_l[randomize]

   
    batch = 49
    #train_tup = (tr_d[0 : 9*batch], tr_l[0 : 9*batch])
    #test_tup  = (tr_d[9*batch+1 : 11*batch+1], tr_l[9*batch+1 : 11*batch+1])
    val_tup   = (tr_d[11*batch+1 : 13*batch+1], tr_l[11*batch+1 : 13*batch+1])
    train_tup = (tr_d[0 : 686], tr_l[0 : 686])
    test_tup  = (tr_d[686 : 833], tr_l[686 : 833])
    val_tup   = (tr_d[833 : 980], tr_l[833 : 980])
 
    return train_tup, test_tup, val_tup
