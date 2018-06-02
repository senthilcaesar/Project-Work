import numpy as np
import time
from math import sqrt
import random

THRESHOLD = 0.5
EPOCH_SKIP = 0
EPOCH_STOP = 0
PRECISION = 0.01
STREAK = 10
MINIMUM = 30


class Network(object):

    def __init__(self, sizes):
        """The list 'sizes' contains the number of neurons in the
        respective layers of the network.  For example, if the list
        was [2, 3, 1] then it would be a three-layer network, with the
        first layer containing 2 neurons, the second layer 3 neurons,
        and the third layer 1 neuron.  The biases and weights for the
        network are initialized randomly, using a Gaussian
        distribution with mean 0, and variance 1.  Note that the first
        layer is assumed to be an input layer, and by convention we
        won't set any biases for those neurons, since biases are only
        ever used in computing the outputs from later layers."""
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        """Return the output of the network if 'a' is input."""
        for b, w in zip(self.biases, self.weights):
            a = self.sigmoid(np.dot(w, a) + b)
        return a

    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations."""
        # why = [[(0 if (y == 1) else 1)], [y]]
        why2 = np.zeros(output_activations.shape)
        why2[0 if (len(output_activations) == 1) else y] = 1
        # print(why2, y)
        # print(output_activations)
        # print(why)
        # print(output_activations - why2)
        return (output_activations - why2)
        # return (output_activations - y)

    def sigmoid_prime(self, z):
        """Derivative of the sigmoid function."""
        return self.sigmoid(z) * (1 - self.sigmoid(z))

    def sigmoid(self, z):
        """The sigmoid function.  Note that when the input z is a
        vector or Numpy array, Numpy automatically applies the
        sigmoid function element-wise (in vectorized form)."""
        return 1.0 / (1.0 + np.exp(-z))

    def SGD(self, training_data, epochs, mini_batch_size,
            eta, verbose, test_data=None):
        """Train the neural network using mini-batch stochastic
        gradient descent.  The 'training_data' is a list of tuples
        '(x, y)' representing the training inputs and the desired
        outputs.  The other non-optional parameters are
        self-explanatory.  If 'test_data' is provided then the
        network will be evaluated against the test data after each
        epoch, and partial progress printed out.  This is useful for
        tracking progress, but slows things down substantially."""

        # Generate a unique run ID based on the current date/time.
        localTime = time.localtime(time.time())
        runID = ('{:04d}{:02d}{:02d}_{:02d}{:02d}'
                 '{:02d}'.format(localTime[0], localTime[1], localTime[2],
                                 localTime[3], localTime[4], localTime[5]))
        if test_data:
            n_test = len(test_data)
        n = len(training_data)
        # qual_check = 0
        # qual_streak = 0
        stats = []

        for j in range(epochs):
            # Here's the formula for the eta that decreases over time.
            # It's not ideal in its current form, but it works.
            moving_eta = ((eta - .05) / epochs) * (epochs - j)
            # qual_start = 0

            random.shuffle(training_data)
            mini_batches = [training_data[k:k + mini_batch_size]
                            for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, moving_eta)
            if test_data:
                TP, TN, FP, FN, TPs, TNs, FPs, FNs = self.evaluate(test_data)
                detR = 0 if (TP == 0) else (TP / (TP + FN))
                falR = 0 if (FP == 0) else (FP / (TP + FP))
                qalR = 0 if (TP == 0) else (TP / (TP + FP + FN))
                log2 = ("{0},{1},{2},{3},{4},{5},{6},{7},"
                        "{8},{9},{10},{11},{12},{13},{14}\n"
                        .format(runID, j, epochs - 1, TP, TN, FP, FN, n_test,
                                detR, falR, qalR,
                                sum(y for (x, y, z) in test_data),
                                int(sqrt(len(training_data[0][0]))),
                                self.sizes, moving_eta))
                log3 = ("{0}\n".format(FNs))
                # log4 = ("{0} {1}\n".format(TPs, TNs))
                with open('../log/log.txt', 'a') as outFile:
                    outFile.write(log2)
                if(j > 70 and qalR > 0.85 and len(log3[0]) > 0):
                    with open('../log/trouble/' + runID + '.txt', 'a') as outFile2:
                        outFile2.write(log3)
                    # with open('../log/good/' + runID + '.txt', 'a') as outFile3:
                    #     outFile3.write(log4)
                if(verbose == 1):
                    log1 = ("ID({}), Epoch({}/{}), "
                            "TP/TN/FP/FN/Tot({:03d}/{:03d}/{:03d}/{:03d}/{:03d}), "
                            "DR/FR/QR({:.3f}/{:.3f}/{:.3f}), "
                            # , FPs({}), FNs({})"
                            "Craters({:03d}), ImgS/Hid,Lay,Rs/ETA({:03d}/{}/{:.2f})"
                            .format(runID, j, epochs - 1, TP, TN, FP, FN, n_test,
                                    detR, falR, qalR,
                                    sum(y for (x, y, z) in test_data),
                                    int(sqrt(len(test_data[0][0]))),
                                    self.sizes, moving_eta))  # , FPs, FNs))
                    print(log1)
                # if EPOCH_STOP:
                #     if j < MINIMUM:
                #         continue
                #     else:
                #         qual_check = abs(qalR - qual_check)
                #         if abs(qalR - qual_start) < PRECISION:
                #             qual_streak = qual_streak + 1
                #         else:
                #             qual_start = qalR
                #         if qual_streak >= STREAK:
                #             print("LOCAL MINIMUM REACHED -- within {0}%% -- for {1} Epochs\n"
                #                   .format(PRECISION, qual_streak))
                #             break
                stats.append([TP, TN, FN, detR, falR, qalR, FP])
                if(j == epochs - 1):
                    return stats
            else:
                print("Epoch {0} complete".format(j))

    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The 'mini_batch' is a list of tuples '(x, y)', and 'eta'
        is the learning rate."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y, z in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w - (eta / len(mini_batch)) * nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - (eta / len(mini_batch)) * nb
                       for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """Return a tuple '(nabla_b, nabla_w)'' representing the
        gradient for the cost function C_x.  'nabla_b' and
        'nabla_w' are layer-by-layer lists of numpy arrays, similar
        to 'self.biases' and 'self.weights'."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x]  # list to store all the activations layer by layer
        zs = []  # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = self.sigmoid(z)
            # print(activation)
            activations.append(activation)
        # backward pass
        delta = (self.cost_derivative(activations[-1], y)
                 * self.sigmoid_prime(zs[-1]))
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book.  Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = self.sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Return the stats based on the performance of the neural
        network."""
        intermediate_results = [(self.feedforward(x), y, z)
                                for (x, y, z) in test_data]
#        for i in range(len(intermediate_results)):
#            print (intermediate_results[i][0], intermediate_results[i][1])
        if(self.sizes[-1] > 1):
            test_results = [(np.argmax(x), y, z, (x[np.argmax(x)] - x[np.argmin(x)])[0])
                            for (x, y, z) in intermediate_results]
        else:
            test_results = [((1 if (x - THRESHOLD > 0) else 0), y, z, x[0][0])
                            for (x, y, z) in intermediate_results]
        tp = tn = fp = fn = 0
        fps = []
        fns = []
        tps = []
        tns = []
        for (x, y, z, xx) in test_results:
            if x == y == 1:
                tp += 1
                tps.append(z)
            if x == y == 0:
                tn += 1
                tns.append(z)
            if x == 1 and y == 0:
                fp += 1
                fps.append(z)
            if x == 0 and y == 1:
                fn += 1
                fns.append(z)
        return (tp, tn, fp, fn, tps, tns, fps, fns)
