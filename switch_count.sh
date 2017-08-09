#!/bin/bash

# --------------------------------------------------------------
# Author:		Senthil Palanivelu                
# Written:		08/02/2017                             
# Last Updated: 	08/07/2017
# Purpose:  		List of switch and associated ports
# --------------------------------------------------------------

filename="ibtopoology_20170728"
switch_1="0xe41d2d03006e7880"
switch_2="0x2c90300ab26b0"
switch_3="0xe41d2d03006e61e0"
TMPFILE="$(mktemp)"
temp_492_6036="$(mktemp)"
temp_6025="$(mktemp)"
temp_8a6_6036="$(mktemp)"

header_function() {
	echo -e '\033[1m ----------------------------------------------------------------------\033[0m'
	echo -e '\033[1m Port Number         |          Name                      |      Type \033[0m'
	echo -e '\033[1m ----------------------------------------------------------------------\033[0m'
}

# Switch adc492:6036
cat $filename | sed -n "/$switch_1/,/^$/{/^$/q; p}" | tail -n +4 | awk '{printf "%-22s %-30s %-30s %15s \n", $1, $2, $4, $NF}' | sed 's/\"/ /g' > $TMPFILE
while read line
	   do
		   a=($(echo $line | tr ',' "\n")) # split line into array
		   printf "%-30s %-33s %-30s\n" "${a[0]}" "${a[3]}" "${a[4]}"  >> $temp_492_6036
done < $TMPFILE

cat $filename | sed -n "/$switch_2/,/^$/{/^$/q; p}" | tail -n +4 | awk '{printf "%-22s %-30s %-30s %15s \n", $1, $2, $4, $NF}' | sed 's/\"/ /g' > $TMPFILE
while read line
	   do
		   a=($(echo $line | tr ',' "\n")) # split line into array
		   printf "%-30s %-33s %-30s\n" "${a[0]}" "${a[3]}" "${a[4]}"  >> $temp_6025
done < $TMPFILE

cat $filename | sed -n "/$switch_3/,/^$/{/^$/q; p}" | tail -n +4 | awk '{printf "%-22s %-30s %-30s %15s \n", $1, $2, $4, $NF}' | sed 's/\"/ /g' > $TMPFILE
while read line
	   do
		   a=($(echo $line | tr ',' "\n")) # split line into array
		   printf "%-30s %-33s %-30s\n" "${a[0]}" "${a[3]}" "${a[4]}"  >> $temp_8a6_6036
done < $TMPFILE

# Display output
echo -e "\033[01;31m Switch = switch-adc492:SX6036\e[0m"
header_function
cat $temp_492_6036
echo
echo -e "\033[01;31m Switch = switch-SX6025\e[0m"
header_function
cat $temp_6025
echo
echo -e "\033[01;31m Switch = switch-adc8a6:SX6036\e[0m"
header_function
cat $temp_8a6_6036
