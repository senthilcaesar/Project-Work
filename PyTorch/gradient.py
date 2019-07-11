import torch

# To create a variable you need to import the below
from torch.autograd import Variable

# Variable is basically wrapper around the tensor that allows it to accumulate gradients
# Gradients are just the slope / derivative of a function

a = Variable(torch.ones((2, 2), requires_grad=True))

# What it means to accumulate gradients ?

x = Variable(torch.tensor(2.0), requires_grad=True)

# Backward should be called only on a scalar (i.e 1-element tensor) or with gradient w.r.t the variable
# For us to calculate the gradient we want to reduce the final output to a single value
y = 9*x**4 + 2*x**3 + 3*x**2 + 6*x + 1

# To compute the derivative of this function at x = 2.0, we simply call y.backward()
y.backward()

# Having computed the derivative at x = 2.0, to access the value we simply call x.grad
print(x.grad)

# This gradient approach will be very handy when implementing gradient descent in neural network
