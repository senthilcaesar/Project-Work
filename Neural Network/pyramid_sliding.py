import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import theano
import theano.tensor as T
from skimage.transform import pyramid_gaussian
import cv2
import cPickle


def sliding_window(image, stepSize, windowSize):
	# slide a window across the image
   for y in xrange(0, image.shape[0], stepSize):
		for x in xrange(0, image.shape[1], stepSize):
			# yield the current window
			yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])
          
def shared(data):
        """Place the data into shared variables.  This allows Theano to copy
        the data to the GPU, if one is available.
        """
        shared_x = theano.shared(
            np.asarray(data, dtype=theano.config.floatX), borrow=True)
        return shared_x
    
k = 0
i = 0
mini_batch_size = 49
f = open('../data/network.cnn', 'rb')
net = cPickle.load(f)
f.close()
img = cv2.imread("../data/images/tile3_25.pgm", 0)
img = img/float(255)
(winW, winH) = (30, 30)

iterable = []
coord_list = []
coord = []

for (i, resized) in enumerate(pyramid_gaussian(img, downscale=1.5)):
    if resized.shape[0] < 40 or resized.shape[1] < 40:
       break
     # x and y are the coordinates of the sliding window
    for (x, y, window) in sliding_window(resized, stepSize=8, windowSize=(winW, winH)):

       if (window.shape[0] == 30 and window.shape[1] == 30):
              window = cv2.resize(window, (100, 100), interpolation=cv2.INTER_CUBIC)
              iterable.append(window.flatten())
              tup = (x, y)
              coord.append(tup)

    
    i += 1
    coord_list.append(coord)
    batch = np.array(iterable)
    batch_size = len(batch)
    extra = 0
    crater = 0
    print
    print 'Pyramid shape = ', resized.shape
    print 'Batch Shape = ', batch.shape
    print 'Batch length = ', batch_size
    
    
    if batch_size < mini_batch_size:
        pad = []
        extra = mini_batch_size - batch_size
        print 'Extra = ', extra
        for k in range(extra):
            pad.append(batch[0])
        batch = np.concatenate([batch, pad])
        batch_size = len(batch)
        print 'New batch length = ', len(batch)
        
    T_batch = shared(batch)
    crater, crater_coord = net.classifier(k, T_batch, mini_batch_size, batch_size, extra, crater, coord)
    print 'Craters seen in Pyramid', i, " = ", crater
    print 'No of the coordinates in Pyramid', i, " = ", len(crater_coord)
    
    f = open('crater_coord.txt', 'a')
    for t in crater_coord:
       line = ' '.join(str(x) for x in t)
       f.write(line + '\n')
    f.close()
    
    iterable = []
    coord = []
    
