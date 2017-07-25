#!/bin/bash

# --------------------------------------------------------------
# Author:		Senthil Palanivelu                 
# Written:		02/07/2016                             
# Last Updated: 	16/10/2016
# Purpose:  		Contact Database Application
# --------------------------------------------------------------

fname="names.dat"
count=0

pause(){

echo -n "Press <ENTER> to continue: "
read xyz

}

yesno()
{
    #
    #   Loop until a valid response is entered
    #
    while :
    do
        #
        echo -n "$* (Y/N)?"
        read yn junk

        case $yn in
            y|Y|yes|Yes|YES)
                return 0
		;;        # return TRUE
            n|N|no|No|NO)
                return 1
		;;        # return FALSE
            *)
                echo Please answer Yes or No.
		;;
          
        esac
    done
}

usage() {

while :
do
if [ $# -le 0 ]
	then
	echo $#
	echo "Usage: Please Input atleast one parameter"
	exit 0
else

for fne in $*
	do
	if [ -f "$fne" ]
	then
		if [ -w "fne" ]
		then
		echo "The file is not Writable"
		exit 0
		else
		return 0
		fi
	fi

	if [ ! -f $fne ]
	then
		echo "File Doesn't exits!"
		if yesno Create the file
		then
		`touch "$fne"`
			if [ -f "$fne" ]
			then
			return 0
			else
			exit 0
			fi
		else
		exit 0
		fi
	fi
	done
fi
done
}

create_record() {               # Function 1


		echo -n "Enter your First name: "
		read firstname
		echo -n "   Enter your surname: "
		read sname
		echo -n "   Enter your Address: "
		read address
		echo -n "      Enter your city: "
		read city
		echo -n "     Enter your state: "
		read state
		echo -n "   Enter your zipcode: "
		read zipcode

# Insert the details into a file
		echo "First Name: $firstname"
		echo "Sur   Name: $sname"
		echo "Address   : $address"
		echo "City      : $city"
		echo "State	: $state"
		echo "ZipCode	: $zipcode"
		echo
		if yesno Are you sure the above details are correct
		then
		echo "$firstname : $sname : $address : $city : $state : $zipcode" >> $fname
		echo
		echo "Record Added into the Database"
		else continue
		fi
		if yesno Would like like to add another record
		then
		create_record
		fi
		
}

view_record(){                 # Function 2

		if [ -f "$fname" ]
                then
                (		
		echo
		echo "Here are the current contacts in the database: "
		echo
                echo "First Name    Surname         Address             City           State Zip"
                echo "============================================================================"
		sort $fname | awk -F : '{printf("%-14.14s%-16.16s%-20.20s%-15.15s%-6.6s%-5.5s\n", $1, $2, $3, $4, $5, $6)}'
		) | more
		echo
		echo "There are `cat $fname | wc -l` contacts in the database"
		else
                echo "No Records were found in the database, The record is empty !!!"
		fi
}

search_record(){              # Function 3

	echo -n "Enter the Pattern: "
	read pattern
	echo
	cat $fname | grep -i $pattern | more
	echo

}

delete_record(){              # Function 4

	echo -n "Enter the Pattern to delete: "
	read pattern
	echo
	cat $fname | grep -i $pattern
	echo
		if yesno Are you sure you want to delete
		then
		cat $fname | sed "/$pattern/d" > /home/sp1989/senthil/tmpfile.txt
		cp tmpfile.txt "$fname"
		echo "The record is deleted"
		fi
}

exit_app() {		      # Function 5

if yesno Are you sure you want to quit
then
	exit 0
fi
}

default_choice() {            # Function 6

	echo Invalid Choice, Try Again Please
}

if usage $*

then
# Menu of Choices
while :
     do
	echo "Choice 1: Create a Record"
	echo "Choice 2: View Records"
	echo "Choice 3: Search for Records"
	echo "Choice 4: Delete Records that macth a pattern"
	echo
	echo -n "Enter you Choice(or q to quit): "
	read choice

		case "$choice" in

# Menu view
#----------
# Create a Record
		1)
		create_record  # Function call 1
		pause
		;;

		2)
		view_record    # Function Call 2
		;;
	
    		3)
		search_record  # Function Call 3
		;;

		4)
		delete_record  # Function Call 4
		;;
	
		q*|Q*)
		exit_app       # Function Call 5
		;;

		*)
		default_choice # Function Call 6
		;;
		esac
	done

 fi
