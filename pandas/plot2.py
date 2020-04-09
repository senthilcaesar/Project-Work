import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 400

df = pd.read_csv('Chapter_1_cleaned_data.csv')

bill_feats = ['BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6']
pay_amt_feats = ['PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']

print(df[bill_feats].describe())
print(df[bill_feats[0]].value_counts())
print(df[bill_feats[0]].value_counts().sort_index())

# Set histogram bin edges
# PLot mutiple histogram
mpl.rcParams['font.size'] = 4
df[bill_feats].hist(bins=20, layout=(2,3), xrot=30)

print(df[bill_feats].describe())
df[pay_amt_feats].hist(layout=(2,3), xrot=30)

pay_zero_mask = df[pay_amt_feats] == 0 
print(pay_zero_mask.sum())
df[pay_amt_feats][~pay_zero_mask].apply(np.log10).hist(layout=(2,3))
