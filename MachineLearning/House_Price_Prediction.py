# Polynomial Regression
# Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dataset = pd.read_csv('HousePrice.txt', sep=" ", header=None)

# Set the Independent variables
X = dataset.iloc[:, 0:2].values

# Set the Dependent variables
Y = dataset.iloc[:, 2].values

# Splitting the Dataset into Training set and Test set
from sklearn.cross_validation import train_test_split
X_train = X[0:100]
X_test = X[101:]
Y_train = Y[0:100]
Y_test = Y[101:]

# Train using Polynomial Regression
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree=3)
X_poly = poly_reg.fit_transform(X_train)
linear_reg2 = LinearRegression()
linear_reg2.fit(X_poly, Y_train)

# Test the test data
poly_reg_pred = PolynomialFeatures(degree=3)
X_pred_poly = poly_reg.fit_transform(X_test)
Y_pred_poly = linear_reg2.predict(X_pred_poly)

print(Y_pred_poly)
