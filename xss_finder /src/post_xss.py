__author__ = 'mohd.siddiqui'
#!/usr/bin/env python


# Imports
import sys, re, urllib2, json, time, cookielib, urllib
from datetime import datetime
from copy import deepcopy
from threadpool import *
from cfghlp import ConfigHelper

# Config
CONFIG_FILE = 'xss.cfg'
config = None
intt=0
# Vars
protocol_secure = 'https://'
protocol_nonsecure = 'http://'
#XSS_RESPONSE="alert('XSS')"

# -------------------------------------
def debug(message):
# -------------------------------------

    if config.get('display', 'debug').lower() == 'true':
        print message

# -------------------------------------
def jsonPrint(json_dict):
# -------------------------------------

    if config.get('display', 'json_pretty_print').lower() == 'true':
        print json.dumps(json_dict, sort_keys=True, indent=4)
    else:
        print json.dumps(json_dict, sort_keys=True, indent=4)

# -------------------------------------
def submit(opener, submit_dict):
# -------------------------------------

    # Init
    request_mode = None
    request_url = None
    request_params = None
    response_mode = None
    response_url = None
    response_params = None

    if 'request' in submit_dict:
        request_protocol = None
        if submit_dict['request'].has_key('use_ssl') and submit_dict['request']['use_ssl'].lower() == 'true':
            request_protocol = protocol_secure
        else:
            request_protocol = protocol_nonsecure
        request_mode = submit_dict['request']['mode']
        request_url = request_protocol + config.get('general', 'base_url') + submit_dict['request']['url']
        request_params = submit_dict['request']['params']
    if 'response' in submit_dict:
        response_protocol = None
        if submit_dict['response'].has_key('use_ssl') and submit_dict['response']['use_ssl'].lower() == 'true':
            response_protocol = protocol_secure
        else:
            response_protocol = protocol_nonsecure
        response_mode = submit_dict['response']['mode']
        response_url = response_protocol + config.get('general', 'base_url') + submit_dict['response']['url']
        response_params = submit_dict['response']['params']

    return_dict = {}
    return_dict['request'] = {'url': request_url, 'mode': request_mode, 'params': request_params}
    if response_url and response_url != request_url:
        return_dict['request_read'] = {'url': response_url, 'mode': response_mode, 'params': response_params}
    t_start = time.time()

    try:
        # Submit Request
        [submit_url, submit_params] = buildRequest(request_mode, request_url, request_params)
        check_url=submit_url+'?'+submit_params
        #print "\nscript url\n",check_url
        response = opener.open(check_url)
        #print response.read()

        # If Response URL is specified, Submit Response
        if response_url and response_url != request_url:
            [submit_url, submit_params] = buildRequest(response_mode, response_url, response_params)
            response = opener.open(submit_url, submit_params)
            if response_url != response.geturl():
                return_dict['request_read']['redirect_url'] = response.geturl()

        # Read Response
        return_dict['response'] = response.readlines()

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception, e:
        return_dict['exception'] = str(e)
    finally:
        t_end = time.time()
        return_dict['time'] = round((t_end - t_start), 5)
        return_dict['timestamp'] = datetime.now().isoformat(' ')

    return return_dict

#--------------------------------------
def buildRequest(mode, url, data):
# -------------------------------------

    if mode == 'GET':
        get_url = '%s?' % (url)
        for k, v in data.iteritems():
            get_url += '%s=%s&' % (k, v)
        if get_url[-1] in ['?', '&']:
            get_url = get_url[:-1]
        return [get_url, None]
    elif mode == 'POST':
        return [url, urllib.urlencode(data)]
    else:
        return [None, None]

# -------------------------------------

# -------------------------------------
def login(openers):
# -------------------------------------



    response_protocol="https://"


    resp_url=response_protocol + config.get('general','base_url') + config.get('login','formkey_url')
    resp=openers['loggedin'].open(resp_url)

    #print "fk_url ",resp_url
    page=resp.read()
    form_key=config.get('general','form_key') #define the form key paramter name within quotes
    __FK = page[page.find(form_key):].split("\"",4)[2] #for finding FK value
    email=config.get('login', 'login_email')
    password=config.get('login', 'login_password')
    opener = openers['loggedin']
    url=response_protocol+config.get('general', 'base_url') + config.get('login', 'login_url')
    login_dict = {'request': {'mode': 'POST', 'url': url, 'use_ssl': 'true',
                              'params': {form_key: __FK,
                                         'email':email,
                                         'password': password}}}
    request_mode = login_dict['request']['mode']
    request_url =  login_dict['request']['url']
    request_params = login_dict['request']['params']
    return_dict = {}
    return_dict['request'] = {'url': request_url, 'mode': request_mode, 'params': request_params}
    [submit_url, submit_params] = buildRequest(request_mode, request_url, request_params)
    #print submit_params
    response = opener.open(submit_url,submit_params)
    return_dict['response'] = response.readlines()
    #print return_dict['response']
    submit_response=return_dict
    submit_response['response'] = json.loads(submit_response['response'][0])
    if submit_response['response']['status'].lower() != 'ok':
        jsonPrint(submit_response)
        sys.exit(0)
    else:
        print "\nYou are now logged in \n"


# -------------------------------------
def attack(site_dict, good_dict ,openers):
# -------------------------------------

    vulnerability_dict={}

    #vulnerability_dict=deepcopy(site_dict)
    vulnerability_dict['vulnerability'] = []
    opener = openers['loggedin']
    [g_submit_url, g_submit_params] = buildRequest(good_dict['request']['mode'],good_dict['request']['post_url'],good_dict['request']['params'])
    opener.open(g_submit_url,g_submit_params)
    request_mode = site_dict['request']['mode']
    request_url =  site_dict['request']['post_url']
    request_params = site_dict['request']['params']
    #vulnerability_dict['url']=site_dict['response']['url']
    vulnerability_dict['params']=request_params
    return_dict = {}
    return_dict['request'] = {'post_url': request_url, 'mode': request_mode, 'params': request_params}
    [submit_url, submit_params] = buildRequest(request_mode, request_url, request_params)
    response = opener.open(submit_url,submit_params)
    opener.open(g_submit_url,g_submit_params)
    #print response.read()
    return_dict['response'] = response.readlines()
    #print "attcked url",submit_url+'?'+submit_params
    response=opener.open(site_dict['response']['url'])
    #good_url=buildRequest(
    #jsonPrint(site_dict)
    #print "----------opening response url------------"
    attack=response.read()
    #print attack
    XSS=site_dict['response']['xss_response']
    #print "\n\nPayload being used is :",XSS

    buf=3
    xs=len(XSS)
    #print "good_dict['response']['xss_response']",good_dict['response']['xss_response']
    XSS_RESPONSE=site_dict['response']['xss_response']

    #print XSS_RESPONSE
#    file = open("test.txt","a")
#    file.write(attack);
#    file.close()
    index = attack.find(XSS_RESPONSE)
    buffer = 20
    attack = attack.split("\n");
    #print len(attack)
    #print "\nindex", index
    #print "\nurl->\n",url
    #print "len(vulnerability_dict['vulnerability'])",len(vulnerability_dict['vulnerability'])
    if index != -1:
        vulnerability_dict['vulnerability'] = True
#    else:
#        print str(index) + "not vulnerable"
    #output={}
    #output['param']

    #Output
    if config.get('display', 'only_show_vulnerable').lower() == 'false' or vulnerability_dict['vulnerability'] ==True or index != -1:

        print "\n===================================================================================="
        print "Vulnerability found (Please check the parameters below)  :"
        jsonPrint(vulnerability_dict)
        intt=1
        print "\n\nPayload being used is :",XSS
        #print "\n\nPage is being searched for this much xss string :",XSS_RESPONSE
        print "\n===================================================================================="

    else:
        print "...."



# -------------------------------------
def attackSequence(sites, payloads, openers):
# -------------------------------------

    # Init
    threadpool = ThreadPool(int(config.get('general', 'max_thread_count')))
    opener=openers['loggedin']
    i=0
    for site in sites:
        site_dict = json.loads(site)
        #print "\n-------->",site_dict
        fk_url=site_dict['request']['fk_url']      #not response url instead fkurl changes need to be made
        #print "\nfk_url-->",fk_url
        resp=opener.open(fk_url)
        page=resp.read()
        form_key=config.get('general','form_key')
        __FK = page[page.find(form_key):].split("\"",4)[2] #for finding FormKey value

        print "\nWorking...."
        #print len(payloads)
        good_dict=deepcopy(site_dict)

        for payload in payloads:
            # Loop through parameters

            #print payload
            for param_k in sorted(site_dict['request']['params'].iterkeys()):
                #print param_k
                attack_dict = deepcopy(site_dict)
                attack_dict['response']['xss_response']=payload
                attack_dict['request']['params'][form_key] =__FK
                #print "\n ------------->",attack_dict
                attack_dict['request']['params'][param_k] = payload
#                print i
#                i+=1
                #jsonPrint(attack_dict)
                #print attack_dict['response']['xss_response']
                threadpool.enqueue(attack, attack_dict,good_dict, openers)
        #print "sites -------->\n",sites

    # Wait for threadpool
    threadpool.wait()

# -------------------------------------
if __name__ == '__main__':
# -------------------------------------

    # Parse Config
    config = ConfigHelper(CONFIG_FILE, False)

    # Init
    debug('Initializing script ...')
    t_global_start = time.time()

    # Load SITES and PAYLOADS files
    sites = []
    sites_file = open(config.get('files', 'sites_file'))
    for site in sites_file:
        site = site[:-1].strip()
        if site[0] != '#':
            sites.append(site)

    payloads = []
    payloads_file = open(config.get('files', 'payloads_file'))
#    for payload in payloads_file:
#        payload = payload[:-1].strip()
#        if payload[0] != '#':
#            payloads.append(payload[:-1])

    for payload in payloads_file:
       payloads.append(payload[:-1])


    # Create Openers
    openers = dict()
#    print "\nYou are being logged into \"%s\" ,testing can only be performed on this domain\n" % config.get('general','base_url')
#    input=str(raw_input("\nAre you sure you want to continue ? Y/N\t"))
    #if input=='Y' or input =='y':

    debug('Creating guest session ...')
    openers['guest'] = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    debug('Creating logged in session ...')
    openers['loggedin'] = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))


    login(openers)
    #take_input()


    # Loop through SITES file
    debug('\nStarting attack sequence ...')
    attackSequence(sites, payloads, openers)


    # Exit
    t_global_end = time.time()
    if (intt=='0'):
        print "\nNo Vulnerabilities found\n"
    debug('Time taken : %.2f seconds' % (t_global_end - t_global_start))
