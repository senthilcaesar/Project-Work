import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import array

def plotDataAndCov(data):
    ACov = np.cov(data, rowvar=False, bias=True)
    print('Covariance matrix:\n', ACov)

    fig, ax = plt.subplots(nrows=1, ncols=2)
    fig.set_size_inches(10, 10)

    ax0 = plt.subplot(2, 2, 1)
    
    # Choosing the colors
    cmap = sns.color_palette("GnBu", 10)
    sns.heatmap(ACov, cmap=cmap, vmin=0)

    ax1 = plt.subplot(2, 2, 2)
    
    # data can include the colors
    if data.shape[1]==3:
        c=data[:,2]
    else:
        c="#0A98BE"
    ax1.scatter(data[:,0], data[:,1], c=c, s=40)
    
    # Remove the top and right axes from the data plot
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

a1 = np.load('/homes/1/sq566/Downloads/case_nmr.npy')

print(a1.min())
values = list()

for i in range(0, 144):
        for j in range(0, 144):
                for k in range(0, 96):
                        values.append(a1[i][j][k])

y = [i for i in range(0, 1990656)]

x = array(values)
y = array(y)

print(x.shape, y.shape)
print(type(x), type(y))

A = np.array([y, x]).T

plotDataAndCov(A)
plt.show()
plt.close()
