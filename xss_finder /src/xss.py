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
        print json.dumps(json_dict, sort_keys=True)

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



    response_protocol="http://"


    resp_url=response_protocol + config.get('general','base_url') + config.get('login','fk_url')
    resp=openers['loggedin'].open(resp_url)

    #print "fk_url ",resp_url
    page=resp.read()
    __FK = page[page.find("__FK"):].split("\"",4)[2] #for finding FK value
    email=config.get('login', 'login_email')
    password=config.get('login', 'login_password')
    opener = openers['loggedin']
    url=response_protocol+config.get('general', 'base_url') + config.get('login', 'login_url')
    login_dict = {'request': {'mode': 'POST', 'url': url, 'use_ssl': 'false',
                              'params': {'__FK': __FK,
                                         'email':email,
                                         'password': password}}}
    request_mode = login_dict['request']['mode']
    request_url =  login_dict['request']['url']
    request_params = login_dict['request']['params']
    return_dict = {}
    return_dict['request'] = {'url': request_url, 'mode': request_mode, 'params': request_params}
    [submit_url, submit_params] = buildRequest(request_mode, request_url, request_params)
    response = opener.open(submit_url,submit_params)
    return_dict['response'] = response.readlines()
    submit_response=return_dict
    submit_response['response'] = json.loads(submit_response['response'][0])
    if submit_response['response']['status'].lower() != 'ok':
        jsonPrint(submit_response)
        sys.exit(0)
    else:
        print "\nYou are now logged in \n"

# -------------------------------------
def attack(site_dict, openers):
# -------------------------------------


    opener = openers['loggedin']
    # Submit request and get response
    submit_response = submit(opener, site_dict)
    #print "\nsubmit_response\n",submit_response
    # Select response (in sites or default)
    expected_xss_responses = "alert('XSS')"
    #print "expected_xss_responses",expected_xss_responses
    # Build vulnerability dict
    #vulnerability_dict = deepcopy(submit_response)
    #print "\nvulnerability_dic",vulnerability_dic
    vulnerability_dict['expected_xss_responses'] = expected_xss_responses
    vulnerability_dict['vulnerability'] = []
    #print "vulnerability_dict['response']",vulnerability_dict
    # Loop through response and search for vulnerabilities
    if vulnerability_dict.has_key('response'):
        a=1
    print "a=====",a
    if vulnerability_dict.has_key('response'):
        del(vulnerability_dict['response'])
        #print "submit_response['response']---",submit_response['response']
        for line_number, line in enumerate(submit_response['response']):
            for expected_xss_response in expected_xss_responses:
                if re.search(expected_xss_response.upper(), line.upper()):
                    vulnerability_dict['vulnerability'].append({'line_number': line_number, 'line': line.strip()})

    # Output
    if config.get('display', 'only_show_vulnerable').lower() == 'false' or len(vulnerability_dict['vulnerability']) > 0:
        jsonPrint(vulnerability_dict)
        intt=1
    else:
        print "...."



# -------------------------------------
def attackSequence(sites, payloads, openers):
# -------------------------------------

    # Init
    threadpool = ThreadPool(int(config.get('general', 'max_thread_count')))
    opener=openers['loggedin']

    for site in sites:
        site_dict = json.loads(site)
        #print "\n-------->",site_dict
        fk_url=site_dict['request']['fk_url']      #not response url instead fkurl changes need to be made
        #print "\nfk_url-->",fk_url
        resp=opener.open(fk_url)
        page=resp.read()
        __FK = page[page.find("__FK"):].split("\"",4)[2] #for finding FK value
        #print __FK
        __FK = urllib.quote_plus(__FK)
        #print "\n__FK   ",__FK
        print "\nWorking...."
        for payload in payloads:
            for param_k in sorted(site_dict['request']['params'].iterkeys()):
                attack_dict = deepcopy(site_dict)
                attack_dict['request']['params']['__FK'] =__FK
                #print "\n ------------->",attack_dict

                attack_dict['request']['params'][param_k] = payload
                threadpool.enqueue(attack, attack_dict, openers)
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
    for payload in payloads_file:
        payload = payload[:-1].strip()
        if payload[0] != '#':
            payloads.append(payload[:-1])

    # Create Openers
    openers = dict()
    print "\nYou are being logged into Test.com make sure you enter testbed urls (else changed config file)\n"
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