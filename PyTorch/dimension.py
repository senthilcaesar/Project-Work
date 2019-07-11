import torch

one_d = torch.arange(0, 9)

# Whats it means to put -1
# It means that I want 3 rows and -1 tells the module that
# please make the decision yourself on how many columns you can allocate with 3 rows
two_d = one_d.view(3, -1)
