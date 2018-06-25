# Polynomial Regression
# Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Importing the Dataset
dataset = pd.read_csv('Position_Salaries.csv')

# Set the Independent variables
X = dataset.iloc[:, 1:2].values

# Set the Dependent variables
Y = dataset.iloc[:, 2].values

# Train using Linear Regression
from sklearn.linear_model import LinearRegression
linear_reg = LinearRegression()
linear_reg.fit(X, Y)

# Visualising the training results
plt.scatter(X, Y, color='red')
plt.plot(X, linear_reg.predict(X), color='blue')
plt.title('Position Level vs Salary - Training set')
plt.xlabel('Position Level')
plt.ylabel('Salary')
plt.show()

# Train using Polynomial Regression
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree=2)
X_poly = poly_reg.fit_transform(X)
linear_reg2 = LinearRegression()
linear_reg2.fit(X_poly, Y)

# Visualising the training results
plt.scatter(X, Y, color='red')
plt.plot(X, linear_reg2.predict(X_poly), color='blue')
plt.title('Position Level vs Salary - Training set')
plt.xlabel('Position Level')
plt.ylabel('Salary')
plt.show()

# Predicting a new result with Linear Regression
linear_reg.predict(6.5)

# Predicting a new result with Polynomial Regression
linear_reg2.predict(poly_reg.fit_transform(6.5))
