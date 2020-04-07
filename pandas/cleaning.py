import pandas as pd

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
