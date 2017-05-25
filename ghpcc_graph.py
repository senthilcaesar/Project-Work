#!/usr/bin/python

# --------------------------------------------------------------
# Author:		      Senthil Palanivelu                 
# Written:		    05/18/2017                             
# Last Updated: 	05/25/2017
# Purpose:  		  Generate graph for GHPCC usage metrics
# --------------------------------------------------------------

import os
import os.path
import sys
import datetime
import commands
import matplotlib.pyplot as plt
import numpy as np

# Enter user input
myData = raw_input('Enter the no of months to generate report: ')

# ------------------------------------------------------- Setting Graph Dimension based on user Input ---------------------------------------------------------#

# Setting range for x and y axis
x = np.arange(int(myData))
y = np.arange(100)

# Set x and y axis limit
plt.xlim(0,int(myData))
plt.ylim(0, 100)

# Empty list for plotting the name in the graph x-axis
my_xticks = []

# X and Y axis title
plt.xlabel('Time')
plt.ylabel('% Percentage')

# -------------------------------------------------------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------Main Program-------------------------------------------------------------------------------#

# Date, Time and Year
now           = datetime.datetime.now()
current_month = now.month
start_year    = now.year

# Array Declaration
month_arr = ['00', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Variables
count   = 1
index_p = 0
num     = 1

# Empty dictionary
my_dict = {}

# Dictionary of users list ( Key is the username and each value associated with the key is a list )
# my_dict Data Structure is similar to Array of Linked List data structure in Java
my_dict.update({'umb_jason_green': 'x1', 'umb_zhongping_lee': 'x2', 'umb_todd_riley': 'x3', 'umb_jill_macoska': 'x4', 'umb_bala_sundaram': 'x5',
                'umb_crystal_schaaf': 'x5', 'umb_bela_torok': 'x6'})

# Initiating the list for each user inside the dictionary
for key in my_dict:
    my_dict[key] = []

print "Generating Graph for the specified months"
print "-------------------------------------------"
while count <= int(myData):
       curr_month_name   = month_arr[current_month]
       prev_month_number = current_month - count - index_p

       if prev_month_number       == 0:
                start_year        = start_year - 1
                prev_month_number = 12
                index_p           = 1                       # Reverse postion of array

       prev_month_name = month_arr[prev_month_number]
       count += 1
       print 'Month: ' + str(prev_month_name) + ', '  + 'Year: ' + str(start_year)
       my_xticks.append(prev_month_name + ' ' + str(start_year))

       # Filter user data and create .dat output file
       file_name = 'Report.' + str(prev_month_name) + '_' + str(start_year)
       if os.path.isfile(file_name):
                cmd         = "cat " + file_name + "|" + "sed -e 1,/Account/d" + "|" + "grep umb" + "|" + "sed 's/\%//g'" + "|" + "awk '$3 > 1'" + "|" "awk '{print $1,$3}'"
                output      = commands.getstatusoutput(cmd)
                output_file = file_name + '.dat'
                f           = open(output_file, 'w')
                for line in output:
                      if line != 0:
                         f.write(line)
                f.close()
       else:
                print file_name + ' file Not found !'
                print 'Error_exit'
                sys.exit()

       # Appending the usage to each user's list in dictionary
       with open(output_file) as data:
             for line in data:
                  line      = line.split()
                  user_name = line[0]
                  my_dict[user_name].append(line[1])

       # Add '0' If the users usage not found during specific month ( Null value is required to plot the graph )
       for key in my_dict:
           if len(my_dict[key]) < count - 1:
                  my_dict[key].append(0)

print "-------------------------------------------"

# Reverse all the list inside the dictionary
for d in my_dict:
    my_dict[d].reverse()

# Un-comment the below for Troubleshooting
# print my_dict

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# -------------------------------------------------------------------- Plotting Graph ------------------------------------------------------------------------------#

# Reversing the list of months
my_xticks.reverse()

# Plot the month name in the x axis
plt.xticks(x, my_xticks)

# Plot graph and legend
for key in my_dict:
   # To check whether the user's list is full of zero's
   bool_val     = all(v == 0 for v in my_dict[key])
   if bool_val == False:
           plot          = plt.plot(x, my_dict[key], marker='o', label = key)
           plt.legend(loc='upper left')

# Set Graph Title
plt.suptitle("HPCC Metrics Graph (" + my_xticks[0] + " - " + my_xticks[-1] + ")", size=16)

# Display Graph
plt.grid()
plt.show()

