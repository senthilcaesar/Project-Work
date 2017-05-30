#!/usr/bin/python

# --------------------------------------------------------------
# Author:		Senthil Palanivelu                 
# Written:		05/18/2017                             
# Last Updated: 	05/30/2017
# Purpose:  		Generate graph for GHPCC usage metrics
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

#----------------------------------------------------------------------Functions-------------------------------------------------------------------------------#

def append_zero(my_dict):
      for key in my_dict:
          if len(my_dict[key]) < r_arr_length - 1:
                 my_dict[key].append(0)

def list_initiate(my_dict):
      for key in my_dict:
          my_dict[key] = []
       
def add_to_dict_dynamic(output_file):
        with open(output_file) as user_data:
                      for line in user_data:
                            line = line.split()
                            name = line[0]
                            value_text = name.partition("_")[2]
                            my_dict.update({name: value_text}) 

def dict_reverse(my_dict):
      for d in my_dict:
           my_dict[d].reverse()

def total_cpu(my_dict_legend):
      for key_s in my_dict_legend:
              total = sum(my_dict_legend[key_s])
              my_dict_sort[key_s] = total

#-------------------------------------------------------------------Main Program-------------------------------------------------------------------------------#

# Date, Time and Year
now           = datetime.datetime.now()
current_month = now.month
start_year    = now.year

# Array Declaration
month_arr = ['00', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Variables
count          = 1
index_p        = 0
num            = 1
r_arr_length   = 2
my_dict        = {}    # This dict stores the user_name as key and CPU % as values
my_dict_legend = {}    # This dict stores the user_name key and CPU hrs as values
my_dict_sort   = {}    # This dict sotres the user_name key and the total cpu hours as values
report_list    = []    # This list stores the report names
                       # my_dict Data Structure is similar to Array of Linked List data structure in Java

print "Generating Graph for the specified months"
print "-------------------------------------------"
while count <= int(myData):                                 # Start of while loop
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
                cmd         = "cat " + file_name + "|" + "sed -e 1,/Account/d" + "|" + "grep umb" + "|" + "sed 's/\%//g'" + "|" + "awk '$3 > 1'" + "|" "awk '{print $1,$2,$3}'"
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
      
       report_list.append(output_file)
       add_to_dict_dynamic(output_file)

print "-------------------------------------------"        # End of while loop

my_dict_legend.update(my_dict)
list_initiate(my_dict)
list_initiate(my_dict_legend)

# Appending the usage to each user's list in dictionary
for output_file in report_list:
    with open(output_file) as data:
         for line in data:
             line      = line.split()
             user_name = line[0]
             my_dict[user_name].append(line[2])
             my_dict_legend[user_name].append(int(line[1]))

         # Add '0' If the users usage not found during specific month ( Null value is required to plot the graph )
         append_zero(my_dict)
         append_zero(my_dict_legend)
         r_arr_length += 1
       
# Reverse all the list inside the dictionary
dict_reverse(my_dict)

# calculate the total CPU hours for each user and add it to my_dict_sort
total_cpu(my_dict_legend)

#------------------------- ---------------------------------------------Troubleshooting---------------------------------------------------------------------------#
#
# print my_dict
# print my_dict_legend
# print my_dict_sort
# result = sorted(my_dict_sort.items(), key=lambda t: t[1], reverse=True)
# for k,v in result:
#    print k,v
# maximum = max(my_dict_sort, key=my_dict_sort.get)  # Just use 'min' instead of 'max' for minimum.
# print(maximum, my_dict_sort[maximum])
#
# -------------------------------------------------------------------- Plotting Graph ------------------------------------------------------------------------------#

# Reversing the list of months
my_xticks.reverse()

# Plot the month name in the x axis
plt.xticks(x, my_xticks)

# Plot graph and legend
# key_l    is the key from the my_dict_sort dictionary in descending order
# bool_val is checked if the list is full of zero's
for key in my_dict:
    result       = sorted(my_dict_sort.items(), key=lambda t: t[1], reverse=True)
    bool_val     = all(v == 0 for v in my_dict[key])
    if bool_val == False:
        for key_l,v in result:
            plot = plt.plot(x, my_dict[key_l], marker='o', label = key_l + " ( " + str(v) + " hrs ) ")
            del my_dict_sort[key_l]
            plt.legend(loc='upper left', title='Total UMB CPU Hours', fancybox=True, prop={'size':16})
            break

# Set Graph Title
plt.suptitle("HPCC Metrics Graph (" + my_xticks[0] + " - " + my_xticks[-1] + ")", size=16)

# Display Graph
plt.grid()
plt.show()
