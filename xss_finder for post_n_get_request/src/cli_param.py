__author__ = 'mohd.siddiqui'
import sys, re, urllib2, json, time, cookielib, urllib
from datetime import datetime
#from threadpool import *
from cfghlp import ConfigHelper



fk_url = str(raw_input("\nType the URL of page where the form is: "))
ssl = fk_url[:5]
#print ssl
if ssl == "https":
    set_ssl = "true"
else:
    set_ssl = "false"

post_url = str(raw_input("\nType in th post URl:  "))
try:
    no_of_params = int(raw_input("\nEnter the no. of parameters that will be submitted(integer only):   "))
except ValueError:
    print "\nYou had to enter a no. please re run the script and be carefull \n"
    sys.exit(0)
    #print no_of_params
a_param = 0
params = dict()
while a_param < no_of_params:
    #print a_param
    key = str(raw_input("\n Enter the param:   "))
    value = str(raw_input("\n Enter the corresponding value: "))
    params[key] = value
    a_param = a_param + 1
p = json.dumps(params, sort_keys=True, indent=4)

login_dict = {}
login_dict = {"request": {}, "response": {}}
#print login_dict
#login_dict["req"]={}
login_dict["request"]["mode"] = 'POST'
login_dict["request"]["fk_url"] = fk_url
login_dict["request"]["use_ssl"] = set_ssl
login_dict["request"]["params"] = params
login_dict["request"]["post_url"] = post_url
#print login_dict
login_dict["response"]["mode"] = "GET"
login_dict["response"]["url"] = fk_url
login_dict["response"]["params"] = ""

s = json.dumps(login_dict)
f = open("sites", 'a')
f.write(s + "\n")
f.close()
