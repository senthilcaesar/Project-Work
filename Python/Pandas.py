import numpy as np
import pandas as pd
from numpy.random import randn

labels = ['a', 'b', 'c']
my_list = [10, 20, 30]
arr = np.array([10, 20, 30])
d = {'a':10, 'b':20, 'c':100}

# Series
series = pd.Series(my_list, index=labels)
x = pd.Series(arr, labels)
my_dict = pd.Series(d)
ser1 = pd.Series(data=[1,2,3,4], index=['USA','CHINA','FRANCE','GERMANY'])
ser2 = pd.Series(data=[1,2,3,4], index=['USA','CHINA','ITALY','JAPAN'])

# Data Frames
df = pd.DataFrame(data=randn(5,4), index=['A','B','C','D','E'], columns=['w','x','y','z'])
print(df[['w','z']])
print(type(df['w']))
print(type(df))

# Create new column
df['new'] = df['w'] + df['y']

# Remove a column
df.drop('new', axis=1, inplace=True)

# Remove a row
df.drop('E', axis=0, inplace=False)

# Selecting a Row
df.loc['A']

# Selecting a row by index
df.iloc[0]

# Select subset of rows and columns
df.loc['B','y']
df.loc[['A','B'],['w','y']]

# Pandas conditional selection in DataFrame
booldf = df > 0
boolw = df['w'] > 0
resultdf = df[boolw]

# All the rows in the DataFrame where z is less than 0
boolz = df['w'] < 0
resultdz = df[boolz]

# Mutiple conditions
mulAnd = df[(df['w'] > 0) & (df['y'] > 1)]
mulOr = df[(df['w'] > 0) | (df['y'] > 1)]

# Resetting index
df.reset_index(inplace=False)

# Set Index
newind = 'CA NY WY OR CO'.split()
df['States'] = newind
df.set_index('States', inplace=True)

# Index levels
outside = ['G1','G1', 'G1', 'G2', 'G2', 'G2']
inside = [1,2,3,1,2,3]
hier_index = list(zip(outside, inside))
hier_index = pd.MultiIndex.from_tuples(hier_index)
df = pd.DataFrame(randn(6,2), hier_index, ['A', 'B'])
df.index.names = ['Groups', 'Num']
df.xs(1, level='Num')

# Missing Data
d = {'A':[1,2,np.nan], 'B':[5,np.nan,np.nan], 'C':[1,2,3]}
df = pd.DataFrame(d)

# drop rows that has null value
df.dropna(axis=1)

# drop columns that has null value
df.dropna(axis=0)

# Replace missing value with the mean of the column
df['A'].fillna(value=df['A'].mean(), inplace=True)

# Learn groupBy with Pandas
data = {'Company':['GOOG','GOOG','MSFT','MSFT','FB','FB'],
        'Person':['Sam','Charlie','Amy','Vanessa','Carl','Sarah'],
        'Sales':[200,120,340,124,243,350]}

df = pd.DataFrame(data)
byComp = df.groupby('Company')
# mean or average sales by company
print(byComp.mean())
# Describe will give a lot of informations
print(df.groupby('Company').describe().transpose())
