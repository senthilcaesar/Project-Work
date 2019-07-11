import torch
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
import torch.nn as nn

n_points = 100
centers = [[-0.5, 0.5], [0.5, -0.5]]
x, y = datasets.make_blobs(n_samples=n_points, random_state=123, centers=centers, cluster_std=0.4)

x_data = torch.tensor(x)
y_data = torch.tensor(y.reshape(100, 1))


class Model(nn.Module):

    def __init__(self, input_size, output_size):
        super().__init__()
        self.linear = nn.Linear(input_size, output_size)

    def forward(self, x):
        pred = torch.sigmoid(self.linear(x))
        return pred


torch.manual_seed(2)
model = Model(2, 1)

[w, b] = model.parameters()
w1, w2 = w.view(2)
b1 = b[0]


def get_params():
    return w1.item(), w2.item(), b1.item()


def scatter_plot():
    plt.scatter(x[y == 0, 0], x[y == 0, 1])
    plt.scatter(x[y == 1, 0], x[y == 1, 1])
    plt.show()


def plot_fit(title):
    plt.title = title
    w1, w2, b1 = get_params()
    x1 = np.array([-2.0, 2.0])
    x2 = (w1 * x1 + b1)/-w2
    plt.plot(x1, x2, 'r')
    scatter_plot()


plot_fit('Inital Model')


# # As you can see the line doesnt perfectly classify the data cluster with
# # the randomly initialized weights and bias
# # We need to use gradient descend to optimize the weight and bias
#
# # First we compute the error of our model
criterion = nn.BCELoss()
#
# # Having computed the error we take its gradient/derivative
# # This steps updates the model weights and bias in the direction of
# # least error
#
# # model.parameters() are the parameters which we wish to update
# # every iteration
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
#
# # Now its time to train out model
#
epochs = 1000
losses = []
model = model.float()
for i in range(epochs):
    # For every epoch we are predicting the output
    y_pred = model.forward(x_data.float())

    # calculating the loss with the ground truth
    loss = criterion(y_pred, y_data.float())
    print("epoch: ", i, "loss ", loss.item())
    losses.append(loss.item())

    optimizer.zero_grad()
    # Having calculated the loss, we must minimize the loss
    loss.backward()

    # Having computed the derivative we update our model parameters through SGD
    optimizer.step()


plot_fit('Inital Model')

plt.plot(range(epochs), losses)
plt.xlabel('Loss')
plt.ylabel('epoch')
plt.show()
