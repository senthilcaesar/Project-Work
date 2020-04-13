import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
mpl.rcParams['figure.dpi'] = 400

df = pd.read_csv('Chapter_1_cleaned_data.csv')
feature_response = df.columns.tolist()

# Remove non-sensical features
items_to_remove = ['ID', 'SEX', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
                   'EDUCATION_CAT', 'graduate school', 'high school',
                   'none', 'others', 'university']

# Use List Comprehension to remove features
feature_response = [item for item in feature_response if item not in items_to_remove]

'''Linear correlation also known as Pearson correlation is used to measure
the strength and direction of the linear relationship between 2 variables'''
corr = df[feature_response].corr()
'''correlation are between -1 and 1'''
# Pearson correlation is only valid for continuous data
#print(corr.iloc[0:5, 0:5])

# Use seaborn to plot correlation
# Stronger linear relationship are closer to 1 or -1
# If there is no linear relationship between 2 variables, the
# correlations will be closer to 0
#sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values, center=0)


'''Perform ANOVA F-test for categorical response variable
F-test is used to perform univariate feature selection'''

X = df[feature_response].iloc[:,:-1].values
y = df[feature_response].iloc[:,-1].values
print(X.shape, y.shape)

from sklearn.feature_selection import f_classif
[f_stat, f_p_value] = f_classif(X, y)
# Create a dataframe using dictionary
f_test_df = pd.DataFrame({'Feature':feature_response[:-1],
                          'F Statistics':f_stat,
                          'p values':f_p_value})
print(f_test_df.sort_values('p values'))

# To select the top 20 % of features according to F-test
from sklearn.feature_selection import SelectPercentile
selector = SelectPercentile(f_classif, percentile=20)
selector.fit(X,y)
best_feature_ix = selector.get_support()
#print(best_feature_ix)

features = feature_response[:-1]
best_features = [features[counter] for counter in range(len(features))
                 if best_feature_ix[counter]]
print(best_features)
