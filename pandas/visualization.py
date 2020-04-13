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

overall_default_rate = df['default payment next month'].mean()
print(overall_default_rate)

group_by_pay_mean_y = df.groupby('PAY_1').agg({'default payment next month': np.mean})
# Mean of the response variable by groups of the PAY_1 feature
print(group_by_pay_mean_y)

#axes = plt.axes()
#axes.axhline(overall_default_rate, color='red')
#group_by_pay_mean_y.plot(marker='x', legend=False, ax=axes)
#axes.set_ylabel('Proportion of credit defaults')
#axes.legend(['Entire dataset', 'Groups of PAY_1'])

pos_mask = y == 1
neg_mask = y == 0
#axes = plt.axes()
#axes.hist(df.loc[neg_mask, 'LIMIT_BAL'], alpha=0.5, color='blue')
#axes.hist(df.loc[pos_mask, 'LIMIT_BAL'], alpha=0.5, color='red')
#axes.tick_params(axis='x', labelrotation=45)
#axes.set_ylabel('Credit limit (NT$)')
#axes.set_xlabel('Number of accounts')
#axes.legend(['Not defaulted', 'Defaulted'])
#axes.set_title('Credit limits by response variable')


bin_edges = list(range(0,850000,50000))
print(bin_edges[-1])
axes = plt.axes()
axes.hist(df.loc[neg_mask, 'LIMIT_BAL'], alpha=0.5, color='blue', bins=bin_edges, density=True)
axes.hist(df.loc[pos_mask, 'LIMIT_BAL'], alpha=0.5, color='red', bins=bin_edges, density=True)
axes.tick_params(axis='x', labelrotation=45)
axes.set_ylabel('Credit limit (NT$)')
axes.set_xlabel('Number of accounts')
y_ticks = axes.get_yticks()
axes.set_yticklabels(np.round(y_ticks*50000,2))
axes.legend(['Not defaulted', 'Defaulted'])
axes.set_title('Normalized distribution of credit limits by response variable')
