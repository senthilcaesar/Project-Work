import numpy as np

F, N = map(int, input().split())
dataset_train = np.array([input().split() for _ in range(N)], float)
T = int(input())
dataset_test = np.array([input().split() for _ in range(T)], float)

X_train = dataset_train[:, 0:F]
Y_train = dataset_train[:, F]
X_test = dataset_test[:, 0:F]

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