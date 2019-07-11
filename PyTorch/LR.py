import torch
import torch.nn as nn


# LR subclass will leverage code from the base class nn.Module
# Module itself will typically act as base class for all neural network module
class LR(nn.Module):

    def __init__(self, input_size, output_size):
        super().__init__()
        self.linear = nn.Linear(input_size, output_size)

    def forward_LR(self, x):
        pred = self.linear(x)
        return pred


torch.manual_seed(1)
model = LR(1, 1)

print(list(model.parameters()))
x = torch.tensor([1.0])
print(model.forward_LR(x))
