# Simple Linear Regression
# Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Importing the Dataset
dataset = pd.read_csv('Salary_data.csv')

# Set the Independent variables
X = dataset.iloc[:, :-1].values

# Set the Dependent variables
Y = dataset.iloc[:, 1].values

# Splitting the Dataset into Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=1/3, random_state=0)

# Train the model using simple linear regression
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, Y_train)

# Test the training data
Y_pred = regressor.predict(X_test)

# Visualising the training results
plt.scatter(X_train, Y_train, color='red')
plt.plot(X_train, regressor.predict(X_train), color='blue')
plt.title('Salary vs Experience - Training set')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()

# Visualising the test results
plt.scatter(X_test, Y_test, color='red')
plt.plot(X_test, Y_pred, color='blue')
plt.title('Salary vs Experience - Test set')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()
