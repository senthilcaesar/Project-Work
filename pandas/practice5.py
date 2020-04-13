import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 400

df = pd.read_csv('Chapter_1_cleaned_data.csv')

print(df['default payment next month'].mean())
print(df['default payment next month'].value_counts())
print(df.groupby('default payment next month')['ID'].count())

from sklearn.linear_model import LogisticRegression
my_lr = LogisticRegression()
my_new_lr =  LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                   intercept_scaling=1, l1_ratio=None, max_iter=100,
                   multi_class='auto', n_jobs=None, penalty='l2',
                   random_state=None, solver='lbfgs', tol=0.0001, verbose=0,
                   warm_start=False)

my_new_lr.C = 0.1
my_new_lr.solver = 'liblinear'
print(my_new_lr)

# .VALUES method returns NumPy arrays
X = df['EDUCATION'][0:10].values.reshape(-1,1)
y = df['default payment next month'][0:10].values

my_new_lr.fit(X, y)
new_X = df['EDUCATION'][10:20].values.reshape(-1,1)
print(my_new_lr.predict(new_X))
