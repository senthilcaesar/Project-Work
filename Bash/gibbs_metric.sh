#!/bin/bash

# --------------------------------------------------------------
# Author:		Senthil Palanivelu               
# Written:		07/06/2017                             
# Last Updated: 	07/07/2017
# Purpose:  		Gibbs Monthly Metrics
# --------------------------------------------------------------

AWK=/bin/gawk
SUBSCRIBERS='it-rc@umb.edu'

curr_month_n=`/bin/date +%m`
prev_month_n=`echo $curr_month_n | $AWK '{printf("%2.2d\n", $1 -1)}'`
curr_year=`/bin/date +%Y`
start_year=$curr_year

if [ $prev_month_n == "00" ]; then
  	prev_month_n=12
  	start_year=`expr $start_year - 1`
fi

MONTHS=(MM Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec)
prev_month_s=${MONTHS[10#$prev_month_n]}

REPORT=Report.${prev_month_s}_${start_year}

start_time=$start_year-$prev_month_n-01
end_time=$start_year-$curr_month_n-01

echo > $REPORT
sreport job sizes PrintJobCount start=$start_time end=$end_time >> $REPORT
echo >> $REPORT
echo >> $REPORT
sreport cluster AccountUtilizationByUser tree start=$start_time end=$end_time -t HourPer >> $REPORT

# Mail to 
cat $REPORT | /bin/mail -s "Gibbs Monthly Metrics for $prev_month_s $start_year" 'senthil.palanivel001@umb.edu'
cat $REPORT | /bin/mail -s "Gibbs Monthly Metrics for $prev_month_s $start_year" $SUBSCRIBERS
