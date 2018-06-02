#!/usr/bin/python3

import os
import sys

# This function returns the value associated to the given variable name
def get_environment_variable_value(variable_name):
        try:
          var_value = os.environ[variable_name]
        except:
          print(variable_name, 'is not an environment variable')
        else:
          return var_value

# This function retun the list of directory contained in PATH variable
def get_dirs_from_path():
        path_var = get_environment_variable_value('PATH')
        return path_var

# This function counts only the number of files in the given directory
def get_file_count(dir_path):
        file_count=0
        os.chdir(dir_path)
        contents = os.listdir('.')
        for entry in contents:
                if not os.path.isdir(entry):
                        file_count += 1
        return file_count

# This function returns a dictionary
def get_file_count_for_dir_list(dir_list):
        dict = {}
        list_dir = dir_list.split(':')
        for dirct in list_dir:
                if os.path.exists(dirct):
                        dict[dirct] = get_file_count(dirct)
        return dict

# This function prints the given dictionary in sorted order
def print_sorted_dictionary(dict):
        for key in sorted(dict.keys()):
                print(key,':',dict[key])

path_dirs = get_dirs_from_path()
dir_count = get_file_count_for_dir_list(path_dirs)
print_sorted_dictionary(dir_count)
