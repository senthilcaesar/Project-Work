#### Libraries
# Standard library
import pickle as cPickle
import gzip
import random

# Third-party libraries
import numpy as np
import theano
import theano.tensor as T
from theano.tensor.nnet import conv2d
from theano.tensor.nnet import softmax
from theano.tensor import shared_randomstreams
from theano.tensor.signal import pool

# Activation functions for neurons
def linear(z): return z
def ReLU(z): return T.maximum(0.0, z)
from theano.tensor.nnet import sigmoid
from theano.tensor import tanh
from crater_loader import load_crater_data_phaseII_wrapper


#### Constants
GPU = True
if GPU:
    print ("Trying to run under a GPU.  If this is not desired, then modify "+\
        "network3.py\nto set the GPU flag to False.")
    try: theano.config.device = 'gpu'
    except: pass # it's already set
    theano.config.floatX = 'float32'
else:
    print ("Running with a CPU.  If this is not desired, then the modify "+\
        "network3.py to set\nthe GPU flag to True.")

#### Load the data

def load_data_shared():
    global train_size, test_size, valid_size
    training_data, test_data, validation_data = load_crater_data_phaseII_wrapper(rotate=1)

    train_size = training_data
    test_size = test_data
    valid_size = validation_data


    def shared(data):
        """Place the data into shared variables.  This allows Theano to copy
        the data to the GPU, if one is available.
        """
        shared_x = theano.shared(
            np.asarray(data[0], dtype=theano.config.floatX), borrow=True)
        shared_y = theano.shared(
            np.asarray(data[1], dtype=theano.config.floatX), borrow=True)
        return shared_x, T.cast(shared_y, "int32")
    return [shared(training_data), shared(validation_data), shared(test_data)]

def load_data_digit(filename="../data/mnist.pkl.gz"):
    f = gzip.open(filename, 'rb')
    training_data, validation_data, test_data = cPickle.load(f)
    f.close()
    def shared(data):
        """Place the data into shared variables.  This allows Theano to copy
        the data to the GPU, if one is available.
        """
        shared_x = theano.shared(
            np.asarray(data[0], dtype=theano.config.floatX), borrow=True)
        shared_y = theano.shared(
            np.asarray(data[1], dtype=theano.config.floatX), borrow=True)
        return shared_x, T.cast(shared_y, "int32")
    return [shared(training_data), shared(validation_data), shared(test_data)]


def check_size_digit(filename="../data/mnist.pkl.gz"):
    f = gzip.open(filename, 'rb')
    training_data, validation_data, test_data = cPickle.load(f)
    f.close()
    return (training_data, validation_data, test_data)

def check_size():
        return (train_size, test_size, valid_size)

#### Main class used to construct and train networks
class Network(object):

    def __init__(self, layers, mini_batch_size):
        """Takes a list of `layers`, describing the network architecture, and
        a value for the `mini_batch_size` to be used during training
        by stochastic gradient descent.
        """
        self.layers = layers
        self.mini_batch_size = mini_batch_size
        # Pamameters for each layer
        self.params = [param for layer in self.layers for param in layer.params]
        self.x = T.matrix("x")
        self.y = T.ivector("y")
        self.l_r = T.scalar("l_r")
        init_layer = self.layers[0]
        # inputs are set one mini-batch at a time

        init_layer.set_inpt(self.x, self.x, self.mini_batch_size)
        for j in range(1, len(self.layers)):
            prev_layer, layer  = self.layers[j-1], self.layers[j]
            layer.set_inpt(
                prev_layer.output, prev_layer.output_dropout, self.mini_batch_size)
        self.output = self.layers[-1].output
        self.output_dropout = self.layers[-1].output_dropout

    
    def classifier(self, k, T_batch, mini_batch_size, batch_size, extra, crater, coord):
	k = T.lscalar()
        self.classify = theano.function(
            [k], self.layers[-1].y_out,
               givens={
                self.x:
                T_batch[k*mini_batch_size: (k+1)*mini_batch_size]
            })
 
        index = 0
        crater_coord = []
        for i in range(batch_size//mini_batch_size):
            predicted_class = self.classify(i)
            if extra == 0:
                predicted_class = predicted_class
            else:
                predicted_class = predicted_class[0:-extra]
            for k in range(len(predicted_class)):
                if (predicted_class[k] == 1):
                       crater += 1
                       crater_coord.append(coord[index+k])
            index += len(predicted_class)
        return crater, crater_coord
        
    
    def SGD(self, training_data, epochs, mini_batch_size, learning_rate,
            validation_data, test_data, lmbda=0.0):
        """Train the network using mini-batch stochastic gradient descent."""


        training_x, training_y = training_data
        validation_x, validation_y = validation_data
        test_x, test_y = test_data
        decay = 0.01
        self.l_r = learning_rate
        #l_r = theano.shared(np.array(learning_rate, dtype=theano.config.floatX))

        # compute number of minibatches for training, validation and testing
        num_training_batches = size(training_data)//mini_batch_size
        num_test_batches = size(test_data)//mini_batch_size
        num_validation_batches = size(validation_data)//mini_batch_size

        print"Number of Train Batch = ", num_training_batches
        print"Number of validation Batch = ", num_validation_batches
        print"Number of Test Batch = ", num_test_batches
        print
        count_test = theano.tensor.extra_ops.bincount(test_y)
        count_train = theano.tensor.extra_ops.bincount(training_y)
        print "Total Non Craters in Training Data = ", count_train[0].eval()
        print "Total Craters in Training Data = ", count_train[1].eval()
        print "Total Non Craters in Test Data = ", count_test[0].eval()
        print "Total Craters in Test Data = ", count_test[1].eval()
        print

        # L2 Regularization: Prevent the model from doing too well on training data
        l2_norm_squared = sum([(layer.w**2).sum() for layer in self.layers])

        # Loss + Regularization
        cost = self.layers[-1].cost(self)+\
                0.5*lmbda*l2_norm_squared/num_training_batches

        # Gradient Descent
        grads = T.grad(cost, self.params)

        # Updating weight and bias
        # updates must be supplied with a list of pairs of the form (shared-variable, new expression).
        # It can also be a dictionary whose keys are shared-variables and values are the new expressions

        #self.vx = theano.shared(np.zeros(0.0, dtype=theano.config.floatX), borrow=True)
        #def velocity(grad):
        #       dx = grad
        #       self.vx = 0.99 * self.vx + dx
        #       return self.vx

        updates = [(param, param-self.l_r*grad) for param, grad in zip(self.params, grads)]

        # Step in the direction of velocity rather than gradient
        #vx = theano.shared(np.asarray(0.0, dtype=theano.config.floatX))
        #for param, grad in zip(self.params, grads):
        #       grad = grad.broadcastable
        #       vx = 600.99 * vx + grad
        #       updates = [(param, param-self.l_r*vx)]


         # Update the Learning Rate
        #updates.append((l_r, l_r * (decay ** epochs)))

        # define functions to train a mini-batch, and to compute the
        # accuracy in validation and test mini-batches.
        i = T.lscalar() # mini-batch index
        train_mb = theano.function(
            [i], cost, updates=updates,
            givens={
                self.x:
                training_x[i*self.mini_batch_size: (i+1)*self.mini_batch_size],
                self.y:
                training_y[i*self.mini_batch_size: (i+1)*self.mini_batch_size]
            })
        validate_mb_accuracy = theano.function(
            [i], self.layers[-1].accuracy(self.y),
            givens={
                self.x:
                validation_x[i*mini_batch_size: (i+1)*mini_batch_size],
                self.y:
                validation_y[i*mini_batch_size: (i+1)*mini_batch_size]
            })
        test_mb_accuracy = theano.function(
            [i], self.layers[-1].accuracy(self.y),
            givens={
                self.x:
                test_x[i*mini_batch_size: (i+1)*mini_batch_size],
                self.y:
                test_y[i*mini_batch_size: (i+1)*mini_batch_size]
            })

         # self.test_mb_predictions(j) will return the predictions for all the samples in the i-th minibatch
        self.test_mb_predictions = theano.function(
            [i], self.layers[-1].y_out,
            givens={
                self.x:
                test_x[i*mini_batch_size: (i+1)*mini_batch_size]
            })

        # Function to get False Negatives
        fn_mb_predictions = theano.function(
            [i], self.layers[-1].true_negative(self.y),
            givens={
                self.x:
                test_x[i*mini_batch_size: (i+1)*mini_batch_size],
                self.y:
                test_y[i*mini_batch_size: (i+1)*mini_batch_size]
            })

        # Function to get False Positives
        fp_mb_predictions = theano.function(
            [i], self.layers[-1].true_positive(self.y),
            givens={
                self.x:
                test_x[i*mini_batch_size: (i+1)*mini_batch_size],
                self.y:
                test_y[i*mini_batch_size: (i+1)*mini_batch_size]
            })


        # Do the actual training
        best_validation_accuracy = 0.0
        for epoch in range(epochs):
            for minibatch_index in range(num_training_batches):
                iteration = num_training_batches*epoch+minibatch_index
                #if iteration % 1000 == 0:
                #print("Training mini-batch number {0}".format(iteration))

                cost_ij = train_mb(minibatch_index)
                #print"Iteration {0}: Cost {1:.4}: l_r {2:.4}".format(iteration, cost_ij, self.l_r)
                if (iteration+1) % num_training_batches == 0:
                    validation_accuracy = np.mean(
                        [validate_mb_accuracy(j) for j in range(num_validation_batches)])
                    #print"Epoch {0}: validation accuracy {1:.2%}".format(
                     #   epoch, validation_accuracy)
                    print"Epoch {0}: Cost {1:.4}: validation accuracy {2:.4}: l_r {3:.4}".format(epoch, cost_ij, validation_accuracy, self.l_r)
                    if validation_accuracy >= best_validation_accuracy:
                        #print"This is the best validation accuracy to date."
                        best_validation_accuracy = validation_accuracy
                        best_iteration = iteration
                        if test_data:
                            test_accuracy = np.mean([test_mb_accuracy(j) for j in range(num_test_batches)])

                            # Softmax layer prediction
                            non_c = 0
                            c = 0
                            tn = 0
                            tp = 0
                            fn = 0
                            fp = 0
                            for j in range(num_test_batches):
                                minibatch_predictions = self.test_mb_predictions(j)
                                f_n = fn_mb_predictions(j)
                                f_p = fp_mb_predictions(j)

                                for k in range(self.mini_batch_size):
                                    if(minibatch_predictions[k] == 0):
                                        non_c += 1
                                    else:
                                        c += 1

                                    if(f_n[k] == True):
                                        fn += 1
                                    if(f_p[k] == True):
                                        fp += 1

                            tn = non_c - fn
                            tp = c - fp
                            #print
                            #print"True Positive  = ", tp
                            #print"True Negative  = ", tn
                            #print"False Negative = ", fn
                            #print"False Positive = ", fp
                            #print
                            #print'The corresponding test accuracy is {0:.2%}'.format(test_accuracy)
        print"Finished training network."
        print"Best validation accuracy of {0:.2%} obtained at iteration {1}".format(
            best_validation_accuracy, best_iteration)
        print"Corresponding test accuracy of {0:.2%}".format(test_accuracy)


#### Define layer types

class ConvPoolLayer(object):
    """Used to create a combination of a convolutional and a max-pooling
    layer.  A more sophisticated implementation would separate the
    two, but for our purposes we'll always use them together, and it
    simplifies the code, so it makes sense to combine them.
    """

    def __init__(self, filter_shape, input_shape, poolsize=(2, 2),
                 activation_fn=ReLU):
        """`filter_shape` is a tuple of length 4, whose entries are the number
        of filters, the number of input feature maps, the filter height, and the
        filter width.
        `input_shape` is a tuple of length 4, whose entries are the
        mini-batch size, the number of input feature maps, the image
        height, and the image width.
        `poolsize` is a tuple of length 2, whose entries are the y and
        x pooling sizes.
        """
        self.filter_shape = filter_shape
        self.input_shape = input_shape
        self.poolsize = poolsize
        self.activation_fn=activation_fn
        # initialize weights and biases
        n_in = (filter_shape[0]*np.prod(filter_shape[2:])/np.prod(poolsize))
        #n_in = filter_shape[0]*np.prod(filter_shape[2:])

        self.w = theano.shared(
            np.asarray(
                np.random.normal(loc=0, scale=np.sqrt(2.0/n_in), size=filter_shape),
                dtype=theano.config.floatX),
            borrow=True)
        self.b = theano.shared(
            np.asarray(
                np.random.normal(loc=0, scale=0.01, size=(filter_shape[0],)),
                dtype=theano.config.floatX),
            borrow=True)
        self.params = [self.w, self.b]

    def set_inpt(self, inpt, inpt_dropout, mini_batch_size):
        self.inpt = inpt.reshape(self.input_shape)
        conv_out = conv2d(
            input=self.inpt, filters=self.w, filter_shape=self.filter_shape,
            input_shape=self.input_shape, border_mode=1)
        pooled_out = pool.pool_2d(
            input=conv_out, ws=self.poolsize, ignore_border=True, stride=(1,1))
        self.output = self.activation_fn(
            pooled_out + self.b.dimshuffle('x', 0, 'x', 'x'))
        self.output_dropout = self.output # no dropout in the convolutional layers

class FullyConnectedLayer(object):

    def __init__(self, n_in, n_out, activation_fn=ReLU, p_dropout=0.0):
        self.n_in = n_in
        self.n_out = n_out
        self.activation_fn = activation_fn
        self.p_dropout = p_dropout
        # Initialize weights and biases
        self.w = theano.shared(
            np.asarray(
                np.random.normal(
                    loc=0.0, scale=np.sqrt(2.0/n_in), size=(n_in, n_out)),
                dtype=theano.config.floatX),
            name='w', borrow=True)
        self.b = theano.shared(
            np.asarray(np.random.normal(loc=0.0, scale=0.01, size=(n_out,)),
                       dtype=theano.config.floatX),
            name='b', borrow=True)
        self.params = [self.w, self.b]

    def set_inpt(self, inpt, inpt_dropout, mini_batch_size):
        self.inpt = inpt.reshape((mini_batch_size, self.n_in))
        self.output = self.activation_fn(
            (1-self.p_dropout)*T.dot(self.inpt, self.w) + self.b)
        self.y_out = T.argmax(self.output, axis=1)
        self.inpt_dropout = dropout_layer(
            inpt_dropout.reshape((mini_batch_size, self.n_in)), self.p_dropout)
        self.output_dropout = self.activation_fn(
            T.dot(self.inpt_dropout, self.w) + self.b)

    def accuracy(self, y):
        "Return the accuracy for the mini-batch."
        return T.mean(T.eq(y, self.y_out))

class SoftmaxLayer(object):

    def __init__(self, n_in, n_out, p_dropout=0.0):
        self.n_in = n_in
        self.n_out = n_out
        self.p_dropout = p_dropout
        # Initialize weights and biases
        self.w = theano.shared(
            np.zeros((n_in, n_out), dtype=theano.config.floatX),
            name='w', borrow=True)
        self.b = theano.shared(
            np.zeros((n_out,), dtype=theano.config.floatX),
            name='b', borrow=True)
        self.params = [self.w, self.b]

    def set_inpt(self, inpt, inpt_dropout, mini_batch_size):
        self.inpt = inpt.reshape((mini_batch_size, self.n_in))

        # self.output use softmax function and retruns the classifier scores as probabilities
        self.output = softmax((1-self.p_dropout)*T.dot(self.inpt, self.w) + self.b)

        self.y_out = T.argmax(self.output, axis=1)

        self.inpt_dropout = dropout_layer(inpt_dropout.reshape((mini_batch_size, self.n_in)), self.p_dropout)

        self.output_dropout = softmax(T.dot(self.inpt_dropout, self.w) + self.b)

    def cost(self, net):
        "Return the log-likelihood cost."
        # Based on the predicted probability by softmax function we compute the Loss using Cross-Entrophy
        return -T.mean(T.log(self.output)[T.arange(net.y.shape[0]), net.y])

    def true_negative(self, y):
        return T.lt(self.y_out, y)

    def true_positive(self, y):
        return T.gt(self.y_out, y)

    def accuracy(self, y):
        "Return the accuracy for the mini-batch."
        return T.mean(T.eq(y, self.y_out))

#### Miscellanea
def size(data):
    "Return the size of the dataset `data`."
    return data[0].get_value(borrow=True).shape[0]

def dropout_layer(layer, p_dropout):
    srng = shared_randomstreams.RandomStreams(
        np.random.RandomState(0).randint(999999))
    mask = srng.binomial(n=1, p=1-p_dropout, size=layer.shape)
    return layer*T.cast(mask, theano.config.floatX)
