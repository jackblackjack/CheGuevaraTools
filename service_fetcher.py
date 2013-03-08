"""
Base class for communicating with a webservice. Set USE_CHARLES_PROXY to true to redirect & inspect traffic going
through an HTTP proxy (e.g. Charles) 
"""

import cookielib
import json
import random
import urllib
import urllib2
import urlparse
import zlib

class ServiceFetcher:

    USE_CHARLES_PROXY = False

    def fetchUrl(self, url, requestType='GET', data={}, headers={}):
        """
        Fetches the url with the given headers and parameters. requestType can be either GET or POST
        """

        # Configure Proxy if any
        if ServiceFetcher.USE_CHARLES_PROXY:
            proxies = {'http':'http://127.0.0.1:8888/'} 
        else:
            proxies = {}

        cookiejar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.ProxyHandler(proxies), urllib2.HTTPCookieProcessor(cookiejar) ) 

        # Set headers
        for header in headers.keys():
            opener.addheaders = [(header, headers[header])]
        urllib2.install_opener(opener) 
        
        # Encode the data and either set it in the URL (GET) or in the body (POST)
        encoded_data = urllib.urlencode(data) 
        if requestType == 'GET':
            if len(encoded_data) > 0:
                url += "?%s" % encoded_data
            response = opener.open(url)
        elif requestType == 'POST':
            response = opener.open(url, encoded_data)

        response_text = response.read()

        # Process response before returning it
        resp_headers = response.info().getheaders
        if resp_headers('Content-Encoding') != []:
            if  'gzip' in resp_headers('Content-Encoding')[0]:
                response_text = zlib.decompress(response_body, 16+zlib.MAX_WBITS)    
        if resp_headers('Content-Type') != []:
            if  'utf8' in resp_headers('Content-Type')[0]:
                response_text = response_text.decode('utf-8')     
        
        return response_text


