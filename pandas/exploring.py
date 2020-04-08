import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 400

filename = 'default_of_credit_card_clients__courseware_version_1_21_19.xls'
df = pd.read_excel(filename, sep=',', decimal='.')

id_counts = df['ID'].value_counts()

# Now we want to get the indices of the duplicated IDs
# to a variable called dupe_mask
dupe_mask = id_counts == 2

# Now we want to select the duplicated IDs using the above boolean mask
dupe_ids = id_counts.index[dupe_mask]
dupe_ids = list(dupe_ids)
print(len(dupe_ids))

# Ipo you have the duplicated IDs in a list
# Next step is to see the what features these duplicate IDs have
# and how those feature values vary among each other

# Diplay the rows in the original df that have the duplicated IDs
# .isin is a series(column) method
# .isin method creates a boolean mask
# .isin method id nested in .loc method
# .loc method to index the rows of the DF by a boolean mask
df.loc[df['ID'].isin(dupe_ids),:].head(10)

# some rows contain all 0's in the column
# a row of all zero is definitely invalid data
# Find all rows that have all zeros except for the 1st column
df_zero_mask = df == 0

# Identify every row where all elements starting from the 2nd column
# are 0
# (:) to examine all wors
# (1:) to examine all columns starting with the second column
# all() method all the column axis ( axis = 1 )
# The iloc indexer for Pandas Dataframe is used for integer-location based indexing / selection by position.
# The iloc indexer syntax is data.iloc[<row selection>, <column selection>]
feature_zero_mask = df_zero_mask.iloc[:,1:].all(axis=1)

# The preceding output tell us that 315 rows have zero for every column but 1 st one
'''Conditional selections with boolean arrays using data.loc[<selection>] is 
the most common method that I use with Pandas DataFrames. With boolean indexing 
or logical selection, you pass an array or Series of True/False values to the .loc 
indexer to select the rows where your Series has True values'''
# Now select all the rows in the orginal df that dont have zeros for all the
# feature and responses
df_clean_1 = df.loc[~feature_zero_mask,:].copy()

# After this we want to know if the number of remaining rows is equal
# to the number of unique IDs
print(df_clean_1.shape)
print(df_clean_1['ID'].nunique())

# Now that we have filtered out the duplicated IDs we are in a postion
# to start looking at the actual data itself


# Final all rows that does not have missing values
print(df_clean_1['PAY_1'].value_counts())
valid_pay_1_mask = df_clean_1['PAY_1'] != 'Not available'

# check how many rows have no missing data
print(sum(valid_pay_1_mask))

df_clean_2 = df_clean_1.loc[valid_pay_1_mask,:].copy()
print(df_clean_2['PAY_1'].value_counts())

# Change column data type
df_clean_2['PAY_1'] = df_clean_2['PAY_1'].astype('int64')
print(df_clean_2[['PAY_1', 'PAY_2']].info())

# Create histogram for 'age' and 'limit_bal'
#df_clean_2[['LIMIT_BAL', 'AGE']].hist()

# Get a tabular summary statistics
print(df_clean_2[['LIMIT_BAL', 'AGE']].describe())

# Get education category
print(df_clean_2['EDUCATION'].value_counts())
# inplace=True ( This means that, instead of returning a new DataFrame
# this operation will make the change on the existing DataFrame )
df_clean_2['EDUCATION'].replace(to_replace=[0,5,6], value=4, inplace=True)
print(df_clean_2['EDUCATION'].value_counts())

# Get marriage
print(df_clean_2['MARRIAGE'].value_counts())
df_clean_2['MARRIAGE'].replace(to_replace=0, value=3, inplace=True)
print(df_clean_2['MARRIAGE'].value_counts())

# check levels of categorical deatures in terms of average values of the response variable
df_clean_2.groupby('EDUCATION').agg({'default payment next month': 'mean'}).plot.bar(legend=False)
plt.ylabel('Default rate')
plt.xlabel('Education level: ordinal encoding')

# Implementing OHE
# 1 = graduate Shcool
# 2 = university
# 3 = high school
# 4 = others
# Insted of doing the above ordinal encodgin for the different education labels
# we will do one hot encoding
df_clean_2['EDUCATION_CAT'] = 'none'
print(df_clean_2[['EDUCATION', 'EDUCATION_CAT']].head(10))

cat_mapping = {
    1: "graduate school",
    2: "university",
    3: "high school",
    4: "others"
    }

# map education numbers to strings
# Examining the string values corresponding to the ordinal encoding of EDUCATION
df_clean_2['EDUCATION_CAT'] = df_clean_2['EDUCATION'].map(cat_mapping)
print(df_clean_2[['EDUCATION', 'EDUCATION_CAT']].head(10))

# Now we are ready to perform OHE
edu_ohe = pd.get_dummies(df_clean_2['EDUCATION_CAT'])
print(edu_ohe.head(10))

# concatenate OHE with df
df_with_ohe = pd.concat([df_clean_2, edu_ohe], axis=1)
print(df_with_ohe[['EDUCATION_CAT', 'graduate school',
             'high school', 'university', 'others']].head(10))

df_with_ohe.to_csv('Chapter_1_cleaned_data.csv', index=False)
