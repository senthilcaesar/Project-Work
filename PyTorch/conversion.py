import numpy as np
import torch

a = np.array([1, 2, 3, 4, 5])

numpy_to_tensor = torch.from_numpy(a)
print(numpy_to_tensor)
print(numpy_to_tensor.type())

tensor_to_numpy = numpy_to_tensor.numpy()
print(tensor_to_numpy)
print(type(tensor_to_numpy))
