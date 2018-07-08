import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pd.core.common.is_list_like = pd.api.types.is_list_like
import datetime

start = datetime.datetime(2012, 1, 1)
end = datetime.datetime(2017, 1, 1)

# Importing the Dataset
tesla = pd.read_csv('Tesla_Stock.csv')
ford = pd.read_csv('Ford_Stock.csv')
gm = pd.read_csv('gm_Stock.csv')

# linear plot of all the stocks Open price.
time = pd.to_datetime(tesla['Date'], format='%Y-%m-%d %H:%M:%S.%f')
plt.plot(time, tesla['Open'], linestyle='-', label='Tesla')
plt.plot(time, ford['Open'], linestyle='-', label='Ford')
plt.plot(time, gm['Open'], linestyle='-', label='GM')
plt.legend(loc='upper left')
plt.title('Opening Price')
plt.xlabel('Date')
plt.ylabel('Open')
plt.show()

# Plot the Volume of stock traded each day
time = pd.to_datetime(tesla['Date'], format='%Y-%m-%d %H:%M:%S.%f')
plt.plot(time, tesla['Volume'], linestyle='-', label='Tesla')
plt.plot(time, ford['Volume'], linestyle='-', label='Ford')
plt.plot(time, gm['Volume'], linestyle='-', label='GM')
plt.legend(loc='upper left')
plt.title('Volume Traded')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.show()

# What was the date of this maximum trading volume for Ford?
index = ford['Volume'].idxmax()
ford_max_vol = ford.iloc[index]
print(ford_max_vol['Date'])

# Create a new column for each dataframe called "Total Traded"
# Total Traded = Open Price * Volume Traded
tesla['Total Traded'] = tesla['Open'] * tesla['Volume']
ford['Total Traded'] = ford['Open'] * ford['Volume']
gm['Total Traded'] = gm['Open'] * gm['Volume']

# Plot the Total Trade against the time index
time = pd.to_datetime(tesla['Date'], format='%Y-%m-%d %H:%M:%S.%f')
plt.plot(time, tesla['Total Traded'], linestyle='-', label='Tesla')
plt.plot(time, ford['Total Traded'], linestyle='-', label='Ford')
plt.plot(time, gm['Total Traded'], linestyle='-', label='GM')
plt.legend(loc='upper left')
plt.title('Total Traded')
plt.xlabel('Date')
plt.ylabel('Total')
plt.show()

# What was the date of this maximum total Trade for Tesla?
index = tesla['Total Traded'].idxmax()
ford_max_vol = ford.iloc[index]
print(ford_max_vol['Date'])

# plotting out some MA (Moving Averages). Plot out the MA50 and MA200 for GM.
gm['MA50'] = gm['Open'].rolling(50).mean()
gm['MA200'] = gm['Open'].rolling(200).mean()
time = pd.to_datetime(gm['Date'], format='%Y-%m-%d %H:%M:%S.%f')
plt.plot(time, gm['Open'], linestyle='-', label='GM-Open')
plt.plot(time, gm['MA50'], linestyle='-', label='GM-MA50')
plt.plot(time, gm['MA200'], linestyle='-', label='GM-MA200')
plt.legend(loc='upper left')
plt.title('Moving Average')
plt.xlabel('Date')
plt.ylabel('Average')
plt.show()

from pandas.plotting import scatter_matrix
#car_comp = pd.concat([tesla["Open"], gm["Open"], ford["Open"]], axis=1)
car_comp.columns = ['Tesla Open', 'GM Open', 'Ford Open']
scatter_matrix(car_comp, alpha=0.2, hist_kwds={'bins':50})

# Basic financial analysis
# r_t = (Pt / Pt-1) -1
# r_t = return at time t
# Pt = Price at time t
# Pt-1 = Price of previous day
# Basically just informs you of percent gain or loss
tesla['returns'] = (tesla['Close'] / tesla['Close'].shift(1)) - 1
ford['returns'] = (ford['Close'] / ford['Close'].shift(1)) - 1
gm['returns'] = (gm['Close'] / gm['Close'].shift(1)) - 1


# Plot the histograms of each of the company returns
plt.hist(tesla['returns'].dropna(), alpha=0.9, color='blue', bins=100, label='Tesla')
plt.hist(ford['returns'].dropna(), alpha=0.9, color='red', bins=100, label='Ford')
plt.hist(gm['returns'].dropna(), alpha=0.9, color='green', bins=100, label='GM')
plt.legend(loc='upper left')
plt.title('Return Historgram')
plt.show()

# Plotting a KDE instead of histograms for another view point. 
# Which stock has the widest plot?
# Ford is little more stable than GM
tesla['returns'].plot(kind='kde', label='Tesla')
ford['returns'].plot(kind='kde', label='ford')
gm['returns'].plot(kind='kde', label='gm')
plt.legend(loc='upper left')
plt.title('Kernel Density Estimation')
plt.show()

# some box plots comparing the returns. 
box_df = pd.concat([tesla["returns"], gm["returns"], ford["returns"]], axis=1)
box_df.columns = ['Tesla Returns', 'GM Returns', 'Ford Returns']
box_df.plot(kind='box')

# Comparing Daily Returns between Stocks
from pandas.plotting import scatter_matrix
scatter_matrix(box_df, alpha=0.9, hist_kwds={'bins':100})
