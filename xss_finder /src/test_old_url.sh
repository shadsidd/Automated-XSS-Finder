#!/bin/sh
filename="sites";

size=$(ls -l $filename | awk '{ print $5 }')
#echo $size
if [ $size -eq '0' ]
    then
        echo 'Running the configuration file  as there is no URL  to test '
        python cli_param.py
fi
python test_xss.py