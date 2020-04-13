import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 400

# Generate Synthetic nosiy linear data
np.random.seed(seed=1)
X = np.random.uniform(low=0.0, high=10.0, size=(1000,))
slope = 0.25
intercept = -1.25
y = slope * X + np.random.normal(loc=0.0, scale=1.0, size=(1000,)) + intercept
plt.scatter(X, y, s=1)

X = X.reshape(-1,1)
from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(X, y)
print("Intercept of the fitted model: ", lin_reg.intercept_)
print("slope of the fitted model: ", lin_reg.coef_)

y_pred = lin_reg.predict(X)
plt.scatter(X, y, s=1)
''' plt.plot produces a line plot by default '''
plt.plot(X, y_pred, 'r')
