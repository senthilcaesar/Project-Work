import crater_deep_network as cdp
import network3


train_size, test_size, validation_size = network3.check_size()

#Print training, test and validation size
cdp.print_size()

#Run experiments
cdp.run_experiments()
