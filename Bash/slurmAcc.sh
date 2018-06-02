#!/bin/bash

# -------------------------------------------------------------------------------------------------------------------------------
# Author:		Senthil Palanivelu             
# Written:		09/25/2016                             
# Last Updated: 	07/07/2017
# Purpose:  		This Script generates No of users, Total Jobs, Total time and CPU Hours for the Gibbs cluster environment
# -------------------------------------------------------------------------------------------------------------------------------

# Local Environmental Variables
BINDIR=/usr/local/bin
AWK=/bin/gawk

# Local Environment Subscribers
SUBSCRIBERS='it-rc@umb.edu'
HOSTNAME="Gibbs"

CURRENT_MONTH=`/bin/date +%m`
PREVIOUS_MONTH=`echo $CURRENT_MONTH | $AWK '{printf("%2.2d\n", $1 - 1)}'`
YEAR=`/bin/date +%Y`
CURRENT_YEAR=$YEAR
START_YEAR=$CURRENT_YEAR

if [ $PREVIOUS_MONTH == "00" ]
	then
		PREVIOUS_MONTH=12
		PREVIOUS_YEAR=`expr $CURRENT_YEAR - 1`
fi

MONTHS=(MM Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec)
PREV_MONTH=${MONTHS[10#$PREVIOUS_MONTH]}

# Navigate to the Torque Accounting Directory
cd '/tmp/accounting'

# Accounting Filenames as YYYYMMDD
MONTHNUMBER=${CURRENT_YEAR}${PREVIOUS_MONTH}
TMPFILE="$(mktemp)"
echo > ${TMPFILE}
FILE_TMP="$(mktemp)"
echo > ${FILE_TMP}

if [ $PREVIOUS_MONTH == "12" ]
	then
	REPORT=Report.${PREV_MONTH}_${PREVIOUS_YEAR}.txt
	START_DATE="$PREVIOUS_YEAR-$PREVIOUS_MONTH-01"
        END_DATE="$CURRENT_YEAR-$CURRENT_MONTH-01"
        START_YEAR=`EXPR $START_YEAR -1`
	else
	REPORT=Report.${PREV_MONTH}_${CURRENT_YEAR}.txt
	START_DATE="$CURRENT_YEAR-$PREVIOUS_MONTH-01"
        END_DATE="$CURRENT_YEAR-$CURRENT_MONTH-01"
fi

echo > ${REPORT} # Create a file called $REPORT

# Reports account utilization and list the underlying usage
sreport cluster AccountUtilizationByUser tree start=$START_DATE end=$END_DATE -t HourPer >> ${REPORT}

# Reports number of jobs by all users
echo >> ${REPORT}
sreport job sizesbyaccount all_cluster start=$START_DATE end=$END_DATE PrintJobCount >> ${REPORT}
echo >> ${REPORT}
echo >> ${REPORT}

echo "Total Number of Job Count by Account: " >> ${REPORT}

sreport job sizesbyaccount all_cluster start=$START_DATE end=$END_DATE PrintJobCount | grep -i "gibbs" > ${TMPFILE}
echo "-------------------------------------" >> ${REPORT}
echo "Cluster    Account" >> ${REPORT}
echo "--------  --------" >> ${REPORT}

cat ${TMPFILE} | while read line
			do
			echo $line | awk '{printf "%-10s %5s %-25.25s\n", $1, $2, "  Total  =  "($3+$4+$5+$6+$7)}' >> ${REPORT}

			echo $line | awk '{print "Total = ", ($3+$4+$5+$6+$7)}' >> ${FILE_TMP}
                        
		done

echo >> ${REPORT}
echo -n "Grand Total               =  " >> ${REPORT}

cat ${FILE_TMP} | awk '{sum += $3} END {print sum}' >> ${REPORT}

#Reports Number of user login details
echo >> ${REPORT}
echo "Number of logins:">>${REPORT}
if [ $PREVIOUS_MONTH == "12" ]
	then
	last -F | grep ${PREV_MONTH} | grep $PREVIOUS_YEAR | sort | awk '{print $1}' | uniq | grep -vE '(runcong|senthil|duse|root|dmcdonald)' | wc -l >> ${REPORT}
	else
	last -F | grep ${PREV_MONTH} | grep $CURRENT_YEAR | sort | awk '{print $1}' | uniq | grep -vE '(runcong|senthil|duse|root|dmcdonald)' | wc -l >> ${REPORT}
fi
echo >> ${REPORT}

# if ls ${MONTHNUMBER}* 1> /dev/null 2>&1 
#		then
#        	echo "">> ${REPORT}
#		else
#       		echo "No Job has been run this month!">> ${REPORT}
#       		#cat ${REPORT} | /bin/mail -s "$HOSTNAME accounting for $PREV_MONTH $START_YEAR" ${SUBSCRIBERS}
#       		exit 2
# fi

cat ${REPORT} | /bin/mail -s "$HOSTNAME accounting for $PREV_MONTH $START_YEAR" 'senthil.palanivel001@umb.edu'
cat ${REPORT} | /bin/mail -s "$HOSTNAME accounting for $PREV_MONTH $START_YEAR" ${SUBSCRIBERS}

cp ${REPORT} ~/

# Remove Temporary file from /tmp/
`rm -rf "$TMPFILE"`
`rm -rf "$FILE_TMP"
