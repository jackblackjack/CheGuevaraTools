"""
Base class for communicating with a webservice. 
"""
import cookielib
import json
import random
import time
import socket
import urllib
import urllib2
import urlparse
import zlib

class ServiceFetcher:
    
    TIMEOUT = 15

    def __init__(self, proxy=None, proxy_protocol='http'):
        """
        
        """
        self.PROXY_URL = proxy # charlie brown 127.0.0.1:8888
        self.PROXY_PROTOCOL = proxy_protocol # http or https
        socket.setdefaulttimeout(self.TIMEOUT) # set socket lib timeout. Also set inurllib2.urlopen

    def fetchURL(self, url, requestType='GET', data={}, headers={}):
        """
        Fetches the url with the given headers and parameters. requestType can be either GET or POST.
        Returns a tuple of the response text (uncompressed) and the response headers.
        """        
        time.sleep(random.randint(1,10))

        # Configure Proxy if any
        if self.PROXY_URL is None:
            proxies = {}
        else:    
            proxies = { self.PROXY_PROTOCOL : self.PROXY_URL} 
        
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
            response = urllib2.urlopen(url, timeout=self.TIMEOUT)
        elif requestType == 'POST':
            response = urllib2.urlopen(url, encoded_data, timeout=self.TIMEOUT)

        response_text = response.read()
        # Process response before returning it
        resp_headers = response.info().getheaders
        if resp_headers('Content-Encoding') != []:
            if  'gzip' in resp_headers('Content-Encoding')[0]:
                response_text = zlib.decompress(response_body, 16+zlib.MAX_WBITS)    

        if resp_headers('Content-Type') != []:
            if  'utf8' in resp_headers('Content-Type')[0]:
                response_text = response_text.decode('utf-8')     
        
        response_headers = dict(response.headers.items())
        # Eval the cookie string into a dict if there is one
        if response_headers.has_key('set-cookie'):
            response_set_cookie =  dict(map(lambda x: ( x.split('=')[0] , '' if len(x.split('=')) == 1 else x.split('=')[1] ), response_headers['set-cookie'].split(';')))
            response_headers['set-cookie'] = response_set_cookie

        return response_text, response_headers


