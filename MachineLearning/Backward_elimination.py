# Multiple Linear Regression
# Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Importing the Dataset
dataset = pd.read_csv('50_Startups.csv')

# Set the Independent variables
X = dataset.iloc[:, :-1].values

# Set the Dependent variables
Y = dataset.iloc[:, 4].values

# Encoding Categorical variable
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X = LabelEncoder()
X[:, 3] = labelencoder_X.fit_transform(X[:, 3])
onehotencoder = OneHotEncoder(categorical_features = [3])
X = onehotencoder.fit_transform(X).toarray()

# Avoiding the dummy variables trap
X = X[:, 1:]

# Splitting the Dataset into Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

# Train the training data using Mutiple Linear Regression
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, Y_train)

# Testing the Test data
Y_pred = regressor.predict(X_test)

# ----------------------Backward Elimination Algorithm------------------------#
import statsmodels.formula.api as sm
X = np.append(np.ones((50,1)).astype(int), X, axis=1)
X_opt = X[:, [0, 1, 2, 3, 4, 5]]
# Step 1 Select the significance level to stay in the model
SL = 0.05
# Step 2 Fit the full model with all possibles predictor
regressor_OLS = sm.OLS(Y, X_opt).fit()
# Step 3 Consider the predictor with highest P-Values
regressor_OLS.summary()
X_opt = X[:, [0, 1, 3, 4, 5]]
regressor_OLS = sm.OLS(Y, X_opt).fit()
regressor_OLS.summary()
X_opt = X[:, [0, 3, 4, 5]]
regressor_OLS = sm.OLS(Y, X_opt).fit()
regressor_OLS.summary()
X_opt = X[:, [0, 3, 5]]
regressor_OLS = sm.OLS(Y, X_opt).fit()
regressor_OLS.summary()
X_opt = X[:, [0, 3]]
regressor_OLS = sm.OLS(Y, X_opt).fit()
regressor_OLS.summary()
