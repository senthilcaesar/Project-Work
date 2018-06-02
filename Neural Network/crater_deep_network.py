from collections import Counter

import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import theano
import theano.tensor as T
from skimage.transform import pyramid_gaussian
from sklearn.externals import joblib
import cv2
import cPickle
import network3
from network3 import sigmoid, tanh, ReLU, Network
from network3 import ConvPoolLayer, FullyConnectedLayer, SoftmaxLayer

training_data, test_data, validation_data = network3.load_data_shared()

def test_drop(mini_batch_size):
        size = 100
        f_s = 7
        padding = 1
        conv_stride = 1
        pool_stride = 1
        pool_size = 4
        n_f1 = 20
        n_f2 = 40
        n_f3 = 80

        co1 = ((size - f_s + 2*padding)/conv_stride) + 1
        po1 = ((co1 - pool_size)/pool_stride) + 1
        print(po1)
        co2 = ((po1 - f_s + 2*padding)/conv_stride) + 1
        po2 = ((co2 - pool_size)/pool_stride) + 1
        print(po2)
        co3 = ((po2 - f_s + 2*padding)/conv_stride) + 1
        po3 = ((co3 - pool_size)/pool_stride) + 1
        print(po3)

        layer1 = ConvPoolLayer(input_shape=(mini_batch_size, 1, size, size),
                      filter_shape=(n_f1, 1, f_s, f_s),
                      poolsize=(4, 4),
                      activation_fn=ReLU)

        layer2 = ConvPoolLayer(input_shape=(mini_batch_size, n_f1, po1 , po1),
                      filter_shape=(n_f2, n_f1, f_s, f_s),
                      poolsize=(4, 4),
                      activation_fn=ReLU)

        layer3 = ConvPoolLayer(input_shape=(mini_batch_size, n_f2, po2 , po2),
                      filter_shape=(n_f3, n_f2, f_s, f_s),
                      poolsize=(4, 4),
                      activation_fn=ReLU)

        layer4 = FullyConnectedLayer(n_in=n_f3*po3*po3, n_out=1000, activation_fn=ReLU, p_dropout=0.0)
        layer5 = FullyConnectedLayer(n_in=1000, n_out=500, activation_fn=ReLU, p_dropout=0.0)
        layer6 = SoftmaxLayer(n_in=500, n_out=2, p_dropout=0.0)

        net = Network([layer1,layer2,layer3,layer4,layer5,layer6],mini_batch_size)
        net.SGD(training_data, 10, mini_batch_size, 0.001, validation_data, test_data, lmbda=0.0)

def test_ding(mini_batch_size):
    
        size = 32
        f_s = 5
        padding = 1
        conv_stride = 1
        pool_stride = 1
        pool_size = 3
        n_f1 = 20
        n_f2 = 40

        co1 = ((size - f_s + 2*padding)/conv_stride) + 1
        po1 = ((co1 - pool_size)/pool_stride) + 1
        #print(po1)
        co2 = ((po1 - f_s + 2*padding)/conv_stride) + 1
        po2 = ((co2 - pool_size)/pool_stride) + 1
        #print(po2)


        layer1 = ConvPoolLayer(input_shape=(mini_batch_size, 1, size, size),
                      filter_shape=(n_f1, 1, f_s, f_s),
                      poolsize=(pool_size, pool_size),
                      activation_fn=ReLU)

        #layer2 = ConvPoolLayer(input_shape=(mini_batch_size, n_f1, po1 , po1),
        #              filter_shape=(n_f2, n_f1, f_s, f_s),
        #              poolsize=(pool_size, pool_size),
        #              activation_fn=ReLU)

        layer3 = FullyConnectedLayer(n_in=n_f1*po1*po1, n_out=500, activation_fn=ReLU, p_dropout=0.0)

        layer4 = SoftmaxLayer(n_in=500, n_out=2, p_dropout=0.0)

        net = Network([layer1,layer3,layer4],mini_batch_size)
        
	net.SGD(training_data, 50, mini_batch_size, 0.3, validation_data, training_data, lmbda=0.0)
    
    
def test_digit(mini_batch_size):

        size = 100
        f_s = 10
        padding = 1
        conv_stride = 1
        pool_stride = 1
        pool_size = 5
        n_f1 = 25
        n_f2 = 50

        co1 = ((size - f_s + 2*padding)/conv_stride) + 1
        po1 = ((co1 - pool_size)/pool_stride) + 1
        co2 = ((po1 - f_s + 2*padding)/conv_stride) + 1
        po2 = ((co2 - pool_size)/pool_stride) + 1
        

        net = Network([
        ConvPoolLayer(input_shape=(mini_batch_size, 1, size, size),
                      filter_shape=(n_f1, 1, f_s, f_s),
                      poolsize=(pool_size, pool_size),
                      activation_fn=ReLU),

        ConvPoolLayer(input_shape=(mini_batch_size, n_f1, po1, po1),
                      filter_shape=(n_f2, n_f1, f_s, f_s),
                      poolsize=(pool_size, pool_size),
                      activation_fn=ReLU),

        FullyConnectedLayer(n_in=n_f2*po2*po2, n_out=500, activation_fn=ReLU, p_dropout=0.0),
        #FullyConnectedLayer(n_in=1000, n_out=1000, activation_fn=ReLU, p_dropout=0.0),

        SoftmaxLayer(n_in=500, n_out=2, p_dropout=0.0)], mini_batch_size)

        net.SGD(training_data, 100, mini_batch_size, 0.01, validation_data, test_data, lmbda=0.0)


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
           
def test_small(mini_batch_size):

        size = 100
        f_s = 5
        padding = 1
        conv_stride = 1
        pool_stride = 1
        pool_size = 3
        n_f1 = 30
        n_f2 = 60

        co1 = ((size - f_s + 2*padding)/conv_stride) + 1
        po1 = ((co1 - pool_size)/pool_stride) + 1
        co2 = ((po1 - f_s + 2*padding)/conv_stride) + 1
        po2 = ((co2 - pool_size)/pool_stride) + 1
        
        net = Network([
        ConvPoolLayer(input_shape=(mini_batch_size, 1, size, size),
                      filter_shape=(n_f1, 1, f_s, f_s),
                      poolsize=(pool_size, pool_size),
                      activation_fn=ReLU),

        ConvPoolLayer(input_shape=(mini_batch_size, n_f1, po1, po1),
                      filter_shape=(n_f2, n_f1, f_s, f_s),
                      poolsize=(pool_size, pool_size),
                      activation_fn=ReLU),
        
        FullyConnectedLayer(n_in=n_f2*po2*po2, n_out=100, activation_fn=ReLU, p_dropout=0.0),

        SoftmaxLayer(n_in=100, n_out=2, p_dropout=0.0)], mini_batch_size)

        net.SGD(training_data, 100, mini_batch_size, 0.01, validation_data, test_data, lmbda=0.0)
        
        f = open('../data/network.cnn', 'wb')
        cPickle.dump(net, f, protocol=2)
        f.close() 

	#k = 0
	#i = 0
	#mini_batch_size = 49
	#f = open('../data/network.cnn', 'rb')
	#net = cPickle.load(f)
	#f.close()
	#img = cv2.imread("../data/images/tile3_25.pgm", 0)
	#img = img/float(255)
	#(winW, winH) = (30, 30)

	#iterable = []
	#coord_list = []
	#coord = []

	#for (i, resized) in enumerate(pyramid_gaussian(img, downscale=1.5)):
    	 # if resized.shape[0] < 40 or resized.shape[1] < 40:
       	#	break
     	# x and y are the coordinates of the sliding window
         # for (x, y, window) in sliding_window(resized, stepSize=8, windowSize=(winW, winH)):

            # if (window.shape[0] == 30 and window.shape[1] == 30):
              #  window = cv2.resize(window, (100, 100), interpolation=cv2.INTER_CUBIC)
             #   iterable.append(window.flatten())
            #    tup = (x, y)
           #     coord.append(tup)


          #i += 1
          #coord_list.append(coord)
    	  #batch = np.array(iterable)
    	  #batch_size = len(batch)
    	  #extra = 0
    	  #crater = 0
    	 # print
    	  #print 'Pyramid shape = ', resized.shape
    	  #print 'Batch Shape = ', batch.shape
    	  #print 'Batch length = ', batch_size


    	 # if batch_size < mini_batch_size:
        #	pad = []
        #	extra = mini_batch_size - batch_size
        #	print 'Extra = ', extra
        #	for k in range(extra):
         #   		pad.append(batch[0])
        #	batch = np.concatenate([batch, pad])
        #	batch_size = len(batch)
        #	print 'New batch length = ', len(batch)

    	  #T_batch = shared(batch)
    	  #crater, crater_coord = net.classifier(k, T_batch, mini_batch_size, batch_size, extra, crater, coord)
    	  #print 'Craters seen in Pyramid', i, " = ", crater
    	  #print 'No of the coordinates in Pyramid', i, " = ", len(crater_coord)

    	  #f = open('crater_coord.txt', 'a')
    	 # for t in crater_coord:
       	#	line = ' '.join(str(x) for x in t)
       	#	f.write(line + '\n')
    	  #f.close()

    	  #iterable = []
    	  #coord = []

def shallow(n=3, epochs=60):
    nets = []
    for j in range(n):
        print("A shallow net with 100 hidden neurons")
        net = Network([
            FullyConnectedLayer(n_in=784, n_out=100),
            SoftmaxLayer(n_in=100, n_out=10)], mini_batch_size)
        net.SGD(
            training_data, epochs, mini_batch_size, 0.1,
            validation_data, test_data)
        nets.append(net)
    return nets

def basic_conv(n=3, epochs=60):
    for j in range(n):
        print ("Conv + FC architecture")
        net = Network([
            ConvPoolLayer(image_shape=(mini_batch_size, 1, 28, 28),
                          filter_shape=(20, 1, 5, 5),
                          poolsize=(2, 2)),
            FullyConnectedLayer(n_in=20*12*12, n_out=100),
            SoftmaxLayer(n_in=100, n_out=10)], mini_batch_size)
        net.SGD(
            training_data, epochs, mini_batch_size, 0.1, validation_data, test_data)
    return net

def omit_FC():
    for j in range(3):
        print ("Conv only, no FC")
        net = Network([
            ConvPoolLayer(image_shape=(mini_batch_size, 1, 28, 28),
                          filter_shape=(20, 1, 5, 5),
                          poolsize=(2, 2)),
            SoftmaxLayer(n_in=20*12*12, n_out=10)], mini_batch_size)
        net.SGD(training_data, 60, mini_batch_size, 0.1, validation_data, test_data)
    return net

def print_size():
    train_size, test_size, validation_size = network3.check_size()
    print'Train data shape       : ', train_size[0].shape
    print'Train labels shape     : ', train_size[1].shape
    print'Test data shape        : ', test_size[0].shape
    print'Test labels shape      : ', test_size[1].shape
    print'Validation data shape  : ', validation_size[0].shape
    print'Validation labels shape: ', validation_size[1].shape
    print

def test_conv(mini_batch_size):
     nets = []
     net = Network([
        # Layer 0
        # 1 Input image of size  = 100 x 100
        # 20 Filters of size     = 5 x 5
        # poolsize               = 2 x 2 ( stride length 2)
        # output of layer 0      = 20 feature Images of size 48 x 48
        ConvPoolLayer(input_shape=(mini_batch_size, 1, 224, 224),
                      filter_shape=(64, 1, 3, 3),
                      poolsize=(2, 2),
                      activation_fn=ReLU),
        # Layer 1
        # 20 Input images of size = 48 x 48
        # 40 Filters of size      = 5 x 5
        # poolsize                = 2 x 2 ( stride length = 2)
        # output of layer 1       = 40 feature Images of size 22 x 22
        ConvPoolLayer(input_shape=(mini_batch_size, 64, 112, 112),
                      filter_shape=(128, 64, 3, 3),
                      poolsize=(2, 2),
                      activation_fn=ReLU),

        ConvPoolLayer(input_shape=(mini_batch_size, 128, 56, 56),
                      filter_shape=(256, 128, 3, 3),
                      poolsize=(2, 2),
                      activation_fn=ReLU),


        ConvPoolLayer(input_shape=(mini_batch_size, 256, 28, 28),
                      filter_shape=(512, 256, 3, 3),
                      poolsize=(2, 2),
                      activation_fn=ReLU),

        ConvPoolLayer(input_shape=(mini_batch_size, 512, 14, 14),
                      filter_shape=(512, 512, 3, 3),
                      poolsize=(2, 2),
                      activation_fn=ReLU),

        # Layer 2
        FullyConnectedLayer(n_in=512*7*7, n_out=4096, activation_fn=ReLU, p_dropout=0.0),

        FullyConnectedLayer(n_in=4096, n_out=1000, activation_fn=ReLU, p_dropout=0.0),

        SoftmaxLayer(n_in=1000, n_out=2, p_dropout=0.0)], mini_batch_size)
        # End of Network Architecture

     net.SGD(training_data, 10, mini_batch_size, 0.01, validation_data, test_data)
     nets.append(net)
     return nets

def test_basic(mini_batch_size):
     nets = []
     net = Network([

        ConvPoolLayer(input_shape=(mini_batch_size, 1, 224, 224),
                      filter_shape=(64, 1, 3, 3),
                      poolsize=(2, 2),
                      activation_fn=ReLU),

        # Layer 2
        FullyConnectedLayer(n_in=64*112*112, n_out=40, activation_fn=ReLU),

        # Activation function
        SoftmaxLayer(n_in=40, n_out=2)], mini_batch_size)
        # End of Network Architecture

     net.SGD(training_data, 10, mini_batch_size, 0.001, validation_data, test_data)
     nets.append(net)
     return nets

def dbl_conv(activation_fn=sigmoid):
    for j in range(3):
        print ("Conv + Conv + FC architecture")
        net = Network([
            ConvPoolLayer(image_shape=(mini_batch_size, 1, 28, 28),
                          filter_shape=(20, 1, 5, 5),
                          poolsize=(2, 2),
                          activation_fn=activation_fn),
            ConvPoolLayer(image_shape=(mini_batch_size, 20, 12, 12),
                          filter_shape=(40, 20, 5, 5),
                          poolsize=(2, 2),
                          activation_fn=activation_fn),
            FullyConnectedLayer(
                n_in=40*4*4, n_out=100, activation_fn=activation_fn),
            SoftmaxLayer(n_in=100, n_out=10)], mini_batch_size)
        net.SGD(training_data, 60, mini_batch_size, 0.1, validation_data, test_data)
    return net

# The following experiment was eventually omitted from the chapter,
# but I've left it in here, since it's an important negative result:
# basic l2 regularization didn't help much.  The reason (I believe) is
# that using convolutional-pooling layers is already a pretty strong
# regularizer.
def regularized_dbl_conv():
    for lmbda in [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0]:
        for j in range(3):
            print ("Conv + Conv + FC num %s, with regularization %s" % (j, lmbda))
            net = Network([
                ConvPoolLayer(image_shape=(mini_batch_size, 1, 28, 28),
                              filter_shape=(20, 1, 5, 5),
                              poolsize=(2, 2)),
                ConvPoolLayer(image_shape=(mini_batch_size, 20, 12, 12),
                              filter_shape=(40, 20, 5, 5),
                              poolsize=(2, 2)),
                FullyConnectedLayer(n_in=40*4*4, n_out=100),
                SoftmaxLayer(n_in=100, n_out=10)], mini_batch_size)
            net.SGD(training_data, 60, mini_batch_size, 0.1, validation_data, test_data, lmbda=lmbda)

def dbl_conv_relu():
    for lmbda in [0.0, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0]:
        for j in range(3):
            print ("Conv + Conv + FC num %s, relu, with regularization %s" % (j, lmbda))
            net = Network([
                ConvPoolLayer(image_shape=(mini_batch_size, 1, 28, 28),
                              filter_shape=(20, 1, 5, 5),
                              poolsize=(2, 2),
                              activation_fn=ReLU),
                ConvPoolLayer(image_shape=(mini_batch_size, 20, 12, 12),
                              filter_shape=(40, 20, 5, 5),
                              poolsize=(2, 2),
                              activation_fn=ReLU),
                FullyConnectedLayer(n_in=40*4*4, n_out=100, activation_fn=ReLU),
                SoftmaxLayer(n_in=100, n_out=10)], mini_batch_size)
            net.SGD(training_data, 60, mini_batch_size, 0.03, validation_data, test_data, lmbda=lmbda)

#### Some subsequent functions may make use of the expanded MNIST
#### data.  That can be generated by running expand_mnist.py.

def expanded_data(n=100):
    """n is the number of neurons in the fully-connected layer.  We'll try
    n=100, 300, and 1000.
    """
    expanded_training_data, _, _ = network3.load_data_shared(
        "../data/mnist_expanded.pkl.gz")
    for j in range(3):
        print ("Training with expanded data, %s neurons in the FC layer, run num %s" % (n, j))
        net = Network([
            ConvPoolLayer(image_shape=(mini_batch_size, 1, 28, 28),
                          filter_shape=(20, 1, 5, 5),
                          poolsize=(2, 2),
                          activation_fn=ReLU),
            ConvPoolLayer(image_shape=(mini_batch_size, 20, 12, 12),
                          filter_shape=(40, 20, 5, 5),
                          poolsize=(2, 2),
                          activation_fn=ReLU),
            FullyConnectedLayer(n_in=40*4*4, n_out=n, activation_fn=ReLU),
            SoftmaxLayer(n_in=n, n_out=10)], mini_batch_size)
        net.SGD(expanded_training_data, 60, mini_batch_size, 0.03,
                validation_data, test_data, lmbda=0.1)
    return net

def expanded_data_double_fc(n=100):
    """n is the number of neurons in both fully-connected layers.  We'll
    try n=100, 300, and 1000.
    """
    expanded_training_data, _, _ = network3.load_data_shared(
        "../data/mnist_expanded.pkl.gz")
    for j in range(3):
        print ("Training with expanded data, %s neurons in two FC layers, run num %s" % (n, j))
        net = Network([
            ConvPoolLayer(image_shape=(mini_batch_size, 1, 28, 28),
                          filter_shape=(20, 1, 5, 5),
                          poolsize=(2, 2),
                          activation_fn=ReLU),
            ConvPoolLayer(image_shape=(mini_batch_size, 20, 12, 12),
                          filter_shape=(40, 20, 5, 5),
                          poolsize=(2, 2),
                          activation_fn=ReLU),
            FullyConnectedLayer(n_in=40*4*4, n_out=n, activation_fn=ReLU),
            FullyConnectedLayer(n_in=n, n_out=n, activation_fn=ReLU),
            SoftmaxLayer(n_in=n, n_out=10)], mini_batch_size)
        net.SGD(expanded_training_data, 60, mini_batch_size, 0.03,
                validation_data, test_data, lmbda=0.1)

def double_fc_dropout(p0, p1, p2, repetitions):
    expanded_training_data, _, _ = network3.load_data_shared(
        "../data/mnist_expanded.pkl.gz")
    nets = []
    for j in range(repetitions):
        print ("\n\nTraining using a dropout network with parameters ",p0,p1,p2)
        print ("Training with expanded data, run num %s" % j)
        net = Network([
            ConvPoolLayer(image_shape=(mini_batch_size, 1, 28, 28),
                          filter_shape=(20, 1, 5, 5),
                          poolsize=(2, 2),
                          activation_fn=ReLU),
            ConvPoolLayer(image_shape=(mini_batch_size, 20, 12, 12),
                          filter_shape=(40, 20, 5, 5),
                          poolsize=(2, 2),
                          activation_fn=ReLU),
            FullyConnectedLayer(
                n_in=40*4*4, n_out=1000, activation_fn=ReLU, p_dropout=p0),
            FullyConnectedLayer(
                n_in=1000, n_out=1000, activation_fn=ReLU, p_dropout=p1),
            SoftmaxLayer(n_in=1000, n_out=10, p_dropout=p2)], mini_batch_size)
        net.SGD(expanded_training_data, 40, mini_batch_size, 0.03,
                validation_data, test_data)
        nets.append(net)
    return nets

def ensemble(nets):
    """Takes as input a list of nets, and then computes the accuracy on
    the test data when classifications are computed by taking a vote
    amongst the nets.  Returns a tuple containing a list of indices
    for test data which is erroneously classified, and a list of the
    corresponding erroneous predictions.
    Note that this is a quick-and-dirty kluge: it'd be more reusable
    (and faster) to define a Theano function taking the vote.  But
    this works.
    """

    test_x, test_y = test_data
    for net in nets:
        i = T.lscalar() # mini-batch index
        net.test_mb_predictions = theano.function(
            [i], net.layers[-1].y_out,
            givens={
                net.x:
                test_x[i*net.mini_batch_size: (i+1)*net.mini_batch_size]
            })
        net.test_predictions = list(np.concatenate(
            [net.test_mb_predictions(i) for i in range(1000)]))
    all_test_predictions = zip(*[net.test_predictions for net in nets])
    def plurality(p): return Counter(p).most_common(1)[0][0]
    plurality_test_predictions = [plurality(p)
                                  for p in all_test_predictions]
    test_y_eval = test_y.eval()
    error_locations = [j for j in range(10000)
                       if plurality_test_predictions[j] != test_y_eval[j]]
    erroneous_predictions = [plurality(all_test_predictions[j])
                             for j in error_locations]
    print ("Accuracy is {:.2%}".format((1-len(error_locations)/10000.0)))
    return error_locations, erroneous_predictions

def plot_errors(error_locations, erroneous_predictions=None):
    test_x, test_y = test_data[0].eval(), test_data[1].eval()
    fig = plt.figure()
    error_images = [np.array(test_x[i]).reshape(28, -1) for i in error_locations]
    n = min(40, len(error_locations))
    for j in range(n):
        ax = plt.subplot2grid((5, 8), (j/8, j % 8))
        ax.matshow(error_images[j], cmap = matplotlib.cm.binary)
        ax.text(24, 5, test_y[error_locations[j]])
        if erroneous_predictions:
            ax.text(24, 24, erroneous_predictions[j])
        plt.xticks(np.array([]))
        plt.yticks(np.array([]))
    plt.tight_layout()
    return plt

def plot_filters(net, layer, x, y):

    """Plot the filters for net after the (convolutional) layer number
    layer.  They are plotted in x by y format.  So, for example, if we
    have 20 filters after layer 0, then we can call show_filters(net, 0, 5, 4) to
    get a 5 by 4 plot of all filters."""
    filters = net.layers[layer].w.eval()
    fig = plt.figure()
    for j in range(len(filters)):
        ax = fig.add_subplot(y, x, j+1)
        ax.matshow(filters[j][0], cmap = matplotlib.cm.binary)
        plt.xticks(np.array([]))
        plt.yticks(np.array([]))
    plt.tight_layout()
    return plt


#### Helper method to run all experiments in the book
def run_experiments():

     nets = test_small(49)

     # plot the filters learned by the first of the nets just trained
#     plt = plot_filters(nets[0], 0, 8, 8)
#     plt.savefig("net_full_layer_0.png")
#     plt = plot_filters(nets[0], 1, 16, 8)
#     plt.savefig("net_full_layer_1.png")

