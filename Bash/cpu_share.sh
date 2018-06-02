#!/bin/bash

# --------------------------------------------------------------
# Author:		Senthil Palanivelu              
# Written:		06/19/2017                             
# Last Updated: 	06/28/2017
# Purpose:  		CPU Share usage
# --------------------------------------------------------------

num="0.0"
TMPFILE="$(mktemp)"
FILE_TMP="$(mktemp)"

file_name=tmp_file
time=`date | awk '{print $4}' | cut -c 1-5`
month=`date | awk '{print $2}'`
day=`date | awk '{print $3}'`

#cpu_file=${file_name}${month}${day}_${time}
cpu_file=${file_name}
touch $cpu_file

total_umass_cpu=`bqueues -r long | awk '/^SHARED_TOP/{c=1} c&&c--' | awk '{print $6}'`

echo > ${cpu_file}
echo -e '\033[1m            CPU Share Usage            \033[0m' >> ${cpu_file}
echo >> ${cpu_file}
echo -e "\033[01;31mTotal CPU Usage by UMass Campus\e[0m" = $total_umass_cpu >> ${cpu_file}
echo >> ${cpu_file}
echo "University             |     CPU Usage" >> ${cpu_file}
echo "--------------------------------------" >> ${cpu_file}

bqueues -r long | awk '/dartmouth/ || /worcester/ || /lowell/ || /boston/ || /amherst/ {c=5} c && c--' | head -n 5 | awk '{print $1, $6}' >> ${TMPFILE}
bqueues -r long | sed -n '/umb_/,/^$/{/^$/q; p}' | awk '{print $1, $6}' >> ${FILE_TMP}

# CPU Usage for the whole UMass Campus
cat ${TMPFILE} | while read line
               do
               echo $line | awk '{printf "%-28s %0s\n", $1, $2}' >> ${cpu_file}
               done
echo >> ${cpu_file}
echo "UMass Boston           |     CPU Usage" >> ${cpu_file}
echo "--------------------------------------" >> ${cpu_file}

# CPU Usage for UMass Boston campus
cat ${FILE_TMP} | while read line
                do
                  a=( $line )
                  if [[ "${a[1]}" != ${num} ]]; then
                     echo $line | awk '{printf "%-28s %0s\n", $1, $2}' >> ${cpu_file}
                  fi
                done

# Percentage of CPU Utilized by UMB Users
echo >> ${cpu_file}
echo "Percentage of CPU Utilized by UMB PI's" >> ${cpu_file}
echo "---------------------------------------" >> ${cpu_file}
total_umass_boston_cpu=`cat ${TMPFILE} | grep -i boston | awk '{print $2}'`
cat ${FILE_TMP} | while read line
                do
                  b=( $line )
                  if [[ "${b[1]}" != ${num} ]]; then
                      top=`echo "${b[1]}" "*" "100" | bc`
                      value=`echo "$top" "/" "$total_umass_boston_cpu" | bc -l | awk '{printf("%.2f\n", $1)}'`
                      printf "%-28s %0s\n" ${b[0]} $value"%" >> ${cpu_file}
                  fi
                done

# Percentage of CPU Utilized by UMass Campus
echo >> ${cpu_file}
echo "Percentage of CPU Utilized by UMass Campus" >> ${cpu_file}
echo "------------------------------------------" >> ${cpu_file}
cat ${TMPFILE} | while read line
                do
                  c=( $line )
                      top=`echo "${c[1]}" "*" "100" | bc`
                      value=`echo "$top" "/" "$total_umass_cpu" | bc -l | awk '{printf("%.2f\n", $1)}'`
                      printf "%-28s %0s\n" ${c[0]} $value"%" >> ${cpu_file}
                done
echo >> ${cpu_file}

# Setting file permission
chmod 755 ${cpu_file}
