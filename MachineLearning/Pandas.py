import numpy as np
import pandas as pd
from numpy.random import randn

labels = ['a', 'b', 'c']
my_list = [10, 20, 30]
arr = np.array([10, 20, 30])
d = {'a':10, 'b':20, 'c':100}

# ------------------------Series--------------------------
series = pd.Series(my_list, index=labels)
x = pd.Series(arr, labels)
my_dict = pd.Series(d)
ser1 = pd.Series(data=[1,2,3,4], index=['USA','CHINA','FRANCE','GERMANY'])
ser2 = pd.Series(data=[1,2,3,4], index=['USA','CHINA','ITALY','JAPAN'])

# -------------------------Data Frames------------------------------
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

# --------------------------Index levels------------------------------------
outside = ['G1','G1', 'G1', 'G2', 'G2', 'G2']
inside = [1,2,3,1,2,3]
hier_index = list(zip(outside, inside))
hier_index = pd.MultiIndex.from_tuples(hier_index)
df = pd.DataFrame(randn(6,2), hier_index, ['A', 'B'])
df.index.names = ['Groups', 'Num']
df.xs(1, level='Num')

#--------------------------- Missing Data---------------------------------
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

# -------------------------Merging, Joining and Concatenating DataFrames---------------------------------
df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                        'B': ['B0', 'B1', 'B2', 'B3'],
                        'C': ['C0', 'C1', 'C2', 'C3'],
                        'D': ['D0', 'D1', 'D2', 'D3']},
                        index=[0, 1, 2, 3])

df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
                        'B': ['B4', 'B5', 'B6', 'B7'],
                        'C': ['C4', 'C5', 'C6', 'C7'],
                        'D': ['D4', 'D5', 'D6', 'D7']},
                         index=[4, 5, 6, 7])

df3 = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
                        'B': ['B8', 'B9', 'B10', 'B11'],
                        'C': ['C8', 'C9', 'C10', 'C11'],
                        'D': ['D8', 'D9', 'D10', 'D11']},
                        index=[8, 9, 10, 11])

# Concatenate DataFrames along rows of same dimensions
pd.concat([df1,df2,df3])
# Concatenate DataFrames along columns of same dimensions
pd.concat([df1,df2,df3], axis=1)

left = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
   
right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                          'C': ['C0', 'C1', 'C2', 'C3'],
                          'D': ['D0', 'D1', 'D2', 'D3']})

# Merge inner join single key
pd.merge(left,right,how='inner',on='key')

left = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                     'key2': ['K0', 'K1', 'K0', 'K1'],
                        'A': ['A0', 'A1', 'A2', 'A3'],
                        'B': ['B0', 'B1', 'B2', 'B3']})
    
right = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                               'key2': ['K0', 'K0', 'K0', 'K0'],
                                  'C': ['C0', 'C1', 'C2', 'C3'],
                                  'D': ['D0', 'D1', 'D2', 'D3']})

# Merge Inner Join mutiple key
pd.merge(left, right, how='inner', on=['key1', 'key2'])

# Joining
left = pd.DataFrame({'A': ['A0', 'A1', 'A2'],
                     'B': ['B0', 'B1', 'B2']},
                      index=['K0', 'K1', 'K2']) 

right = pd.DataFrame({'C': ['C0', 'C2', 'C3'],
                    'D': ['D0', 'D2', 'D3']},
                      index=['K0', 'K2', 'K3'])

# left join
left.join(right)
left.join(right, how='outer')

# ------------------Pandas Common Operations-------------------------------
d = {'col1':[1,2,3,4],
     'col2':[444,555,666,444],
     'col3':['abc','def','ghi','xyz']}

df = pd.DataFrame(d)
# Finding unique values in a DataFrame
df['col2'].unique()
# No of unique elements in a column
df['col2'].nunique()
# How many times each unique value appreared ina column
df['col2'].value_counts()

# Apply custom Method to DataFrames
def times2(x):
    return x*2
df['col2'].apply(times2)

# Corresponding lamba expression of times2 method
express = lambda x:x*2
df['col2'].apply(express)

# Sorting and ordering in Data Frame
df.sort_values(by='col2')

# Find null values
df.isnull()

# Pivot Tables
data = {'A':['foo','foo','foo','bar','bar','bar'],
     'B':['one','one','two','two','one','one'],
       'C':['x','y','x','y','x','y'],
       'D':[1,3,2,5,4,1]}

df = pd.DataFrame(data)
df.pivot_table(values='D', index=['A','B'], columns=['C'])
