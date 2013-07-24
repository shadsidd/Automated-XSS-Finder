#!/usr/bin/env python



# Imports
import sys, re, urllib2, urlparse, json, time, httplib,cookielib,urllib
#from threadpool import *

i=0
# Config
DEBUG = True
MAX_THREAD_COUNT = 1
SITES_FILENAME = str(sys.argv[1])
#print SITES_FILENAME
#sys.exit()
PAYLOADS_FILENAME = 'get_payload'
SCHEME_DELIMITER = '://'
XSS_RESPONSE = "alert('XSS')"

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

intt=0
# -------------------------------------
def attack(url, payload):
# -------------------------------------

    t_start = time.time()
    #print "in attak"
    return_dict = dict()
    return_dict['url'] = url
    #print "..."
#return_dict['url_data'] = data
    return_dict['vulnerability'] = False
    #print "\n url",url
    #print "\n payload" ,payload
    #print "going to try\n"
    #post_url='http://site.com '   # the url in which XSS test needs to be done and it is different from url where we posted params
    try:
        return_dict['method'] = 'GET'
        XSS_RESPONSE=payload
        #print "payload--->", payload
        attack= urllib2.urlopen(url).read()
        #print "\nURL being hit :",url
        print_url=url.replace("<","&lt")
        print "\nURL being hit :",print_url
        #print XSS_RESPONSE
        index = attack.find(XSS_RESPONSE)

        buffer = 20

        attack = attack.split("\n");
        len(attack)
        #print "\nurl->\n",url
        if index != -1:
            intt +=1
            return_dict[' vulnerability'] = True
            print "\n\n--------------------------------------------------------------------------"
            print "\nThis url seems vulnerable\n\n",url
            print "--------------------------------------------------------------------------\n\n"
            #return_dict['vulnerability_data'] = line.strip()
            #print "payload found\n", attack[index-buffer:index+len(XSS_RESPONSE)+buffer]

            #print intt
    #        break

            #print "here"
        t_end = time.time()
        return_dict['time'] = round((t_end - t_start), 2)

    except KeyboardInterrupt, ke:
        sys.exit(0)
    except Exception, e:
        return_dict['exception'] = str(e)


# -------------------------------------
if __name__ == '__main__':
# -------------------------------------
    print "<h1>Python</h1>";
    #exit(0);
    # Init
    t_global_start = time.time()

    sites_file = open(SITES_FILENAME)
    payloads_file = open(PAYLOADS_FILENAME)
    #threadpool = ThreadPool(MAX_THREAD_COUNT)

    # Load SITES and PAYLOADS files
    sites = []
#    input = str(raw_input("\nEnter the URLS you want to test\n"))
#    sites = []

    for site in sites_file:
        sites.append(site[:-1])
        #print "\nsites:", sites
    #sites = input
    print "\nWorking..."
    sys.stdout.flush()
    #exit(0);
    payloads = []

    for payload in payloads_file:
        payloads.append(payload[:-1])

        # Loop through sites

        # Extract Base URL and Parameters from site
    #print "sites len : " + str(len(sites))
    try:
        for site in sites:
            #print site
            parse_url = urlparse.urlparse(site)

            #print mode
            base_url = '%s%s%s%s' % (parse_url.scheme, SCHEME_DELIMITER, parse_url.netloc, parse_url.path)
            #print base_url
            param_parse_list = urlparse.urlparse(site)[4].split('&')
            #print "\nparam_parse_list:",param_parse_list
            param_dict = dict()
            for param_parse_entry in param_parse_list:
                tmp = param_parse_entry.split('=')
                param_dict[tmp[0]] = tmp[1]

            # Loop through payloads
            #print payloads

            for payload in payloads:
                    # Loop through parameters
                #print i
                for k1, v1 in iter(sorted(param_dict.iteritems())):
                            # Build GET param string and POST param dict
                    get_params = ''
                    #post_params = dict()
                    for k2, v2 in iter(sorted(param_dict.iteritems())):
                        if k1 == k2:
                            get_params += '%s=%s&' % (k2, payload)
                            #post_params[k2] = payload
                        else:
                            get_params += '%s=%s&' % (k2, v2)
                            #post_params[k2] = v2

                    get_params = get_params[:-1]
                    #print get_params
                            # Enqueue GET attack
                    #base_url=mode + base_url
                    #print mode
                    #print base_url
                    get_attack_url = '%s?%s' % (base_url, get_params)
                    print_payload=payload.replace("<","&lt")
                    #print "Testing with payload>", print_payload;    #    to see what payload is being used
                    sys.stdout.flush()
                    #threadpool.enqueue(attack, get_attack_url, payload)
                    #print "..."
                    attack(get_attack_url, payload)

                            # Enqueue POST attack
                            #post_attack_url = '%s' % (base_url)

                            #threadpool.enqueue(attack, post_attack_url, post_params)
                            #attack(post_attack_url,post_params)

        # Wait for threadpool
        #threadpool.wait()
    except Exception,e:
        print "\nSome Error , \n\n Please re run the script ",e
    # Exit
    t_global_end = time.time()
    #if DEBUG:
    #print "int->",int
    if(intt == 0):
        print "\n\tNothing Found! \n"

    print 'Time taken : %.2f seconds' % (t_global_end - t_global_start)
