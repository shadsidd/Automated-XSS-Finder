__author__ = 'mohd.siddiqui'
import sys, re, urllib2, json, time, cookielib, urllib
from datetime import datetime
#from threadpool import *
from cfghlp import ConfigHelper


CONFIG_FILE = 'xss.cfg'
config = None

config = ConfigHelper(CONFIG_FILE, False)
a=config.get('general','base_url')
domain=a
print "\nYou will be logged in \"%s\" ,testing can only be performed on this domain\n" % domain
input=str(raw_input("\nAre you sure you want to continue ?(Press N to change the testign enviornment) Y/N \t"))
if input=='Y' or input =='y':
    exit(1)
else:
        print "\n 1.Please make required changes in \".xss.cfg\" file . \n 2.Change the \"base_url\" to the URL (enviornment) you want to test\"\n 3.Change the login credentials \"email\" and \"password\" to valid ones \n 4.Save and re-run this script\n"
        exit (0)