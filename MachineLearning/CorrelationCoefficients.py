# Pearson’s Correlation Coefficients formula
# Measure how strong a relationship is between two variables
import numpy as np

X = np.array([15, 12, 8, 8, 7, 7, 7, 6, 5, 3])
Y = np.array([10, 25, 17, 11, 13, 17, 20, 13, 9, 15])
X_sum = np.sum(X)
Y_sum = np.sum(Y)
XY_sum = np.sum(X*Y)
X_square_sum = np.sum(X**2)
Y_square_sum = np.sum(Y**2)
n = len(X)
numerator = (n*XY_sum) - (X_sum*Y_sum)
denominator = ((n*X_square_sum) - (X_sum**2)) * ((n*Y_square_sum) - (Y_sum**2))
r = numerator / np.sqrt(denominator)
print(r)
