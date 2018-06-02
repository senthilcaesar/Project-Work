#!/usr/bin/env python


from crater_loader import load_crater_data_wrapper
from crater_network import Network
from pre_processing import preprocess
from plot import plot


def runIt(image_size, hidden_layers, output_neurons, starting_eta,
          epochs, mini_batch_size, network_runs, rotate, contrast,
          brightness, verbose):
    """Parameter 'image_size' sets the length and width of the image.
    Parameter 'hidden_layers' is a tuple of hidden layer sizes.  Parameter
    'starting_eta' sets the initial value for the learning rate.  eta will
    decrease as a function of the epochs progress (either on a curve or
    linearly). Parameter 'network_runs' sets the number of full
    RandomData -> TrainNetwork -> TestNetwork cycles are considered.
    This method calls the load_crater_data_wrapper method from crater_loader, 
    arranges the layers, initializes a new network, then trains and tests 
    the network."""

    preprocess(image_size, contrast, brightness)
    all_stats = []
    for _ in range(0, network_runs):
        if(verbose == 0):
            print('Training network - run {}.'.format(_))
        training_data, valid_data, test_data = (
            load_crater_data_wrapper(rotate))
        size_list = (image_size**2,) + hidden_layers + (output_neurons,)
        net = Network(size_list)
        stats = net.SGD(training_data, epochs, mini_batch_size,
                        starting_eta, verbose, test_data)
        all_stats.append(stats)
    plot(all_stats)


if __name__ == '__main__':
    # Set the initial values
    image_size = 150
    hidden_layers = (30, 20)
    output_neurons = 2
    starting_eta = 1.5
    epochs = 10
    mini_batch_size = 50
    network_runs = 1
    rotate = 0   # 1 means yes. 0 means no.
    contrast = 1.5
    brightness = 1
    verbose = 0  # 1 for lots of console output. 0 for basic output.

    runIt(image_size, hidden_layers, output_neurons, starting_eta, epochs,
          mini_batch_size, network_runs, rotate, contrast,
          brightness, verbose)
