#!/bin/sh
filename="sites";
 echo '\n\n What do you want to test ?'
 echo '\n1. GET urls (URLs were params are in url )\n'
 echo '2. POST urls ()\n'
 echo ' Your Choice'
 read test

 if [ $test -eq '2' ]
 then
    size=$(ls -l $filename | awk '{ print $5 }')
    #echo $size
    if [ $size -gt '0' ]
        then
            echo '\nThere is already some URL to test in "sites" file \n1.Do you want to test them \n2. Do you want to test a new URL ?\n'
            read input
            if [ $input -eq '1' ]
                then
                    python check_domain.py
                    a=$?
                     if [ $a -eq '1' ]
                        then
                            python post_xss.py
                    else
                    #python cli_param.py
                        exit 1
                    fi
            elif [ $input -eq '2' ]
                then
                    #echo 'Do you want to enter parameters in CLI mode or want to edit '
                    echo '\n\nRunning the configuration file  and removing the previous content copying all your previous content to old_sites file'
                    cat sites>>old_sites
                    > sites
                    python cli_param.py
                    #python test_xss.py
                    #exit 1
            else
                echo '\n Wrong Input'
            fi
    elif [ $size -eq '0' ]
        then
            echo 'Running the configuration file  as there is nothing to test '
            python check_domain.py
            python cli_param.py
            #python test_xss.py
    fi

 elif [ $test -eq '1' ]
 then
    python get_xss.py
    exit 1
 else
 echo '\nWrong input re-run the script\n'
 fi
 python test_xss.py