"""
ThreadedServiceFetcher is a subclass of thread. It fetches a list of urls using 
ServiceFetcher object via a specified proxy, scrapes the data into a hash and returns
a parent hash with the urls fetched as keys and the hash returned by the scraper as
values.

ThreadedServiceFetcherManager breaks down the list of urls into k groups before assigning
them to k threads (i.e. ThreadedServiceFetcher objects)

   ThreadedServiceFetcherManager([url1, url2, url3,..], scraper_class, path_to_proxies)

See example.py

"""

import colorama
import service_fetcher
import proxy_loader
import threading
import datetime
import time
import traceback
import pdb
from itertools import cycle

class ThreadedServiceFetcher(threading.Thread):

    @staticmethod
    def log(message, color):
        print color + message + colorama.Fore.WHITE
    
    def __init__(self, urls, proxy, scraper_class, req_method='GET', post_data={}, req_headers={}):
        self.urls = urls
        self.proxy = proxy
        self.data = {}
        self.req_method = req_method
        self.post_data = post_data
        self.req_headers = req_headers
        self.scraper_class = scraper_class
        super(ThreadedServiceFetcher, self).__init__()

    def run(self):
        for index, url in enumerate(self.urls):
            try:
                # Fetch the URL using the specified proxy and headers if any
                sf = service_fetcher.ServiceFetcher(self.proxy)
                response, headers = sf.fetchURL(url, self.req_method, self.post_data, self.req_headers)
            except:
                message = "%s/%s - Connection to [%s] via proxy %s failed " % \
                    (index, len(self.urls), url, self. proxy) 
                ThreadedServiceFetcher.log(message, colorama.Fore.MAGENTA)
                # Set URL response to None and move on to the next one
                self.data[url] = None
                continue
            
            try:
                # Feed the response to the scraper method
                scraped_data = self.scraper_class.scrape(response)
                self.data[url] = scraped_data
                message = "%s/%s - Scraping [%s] succeeded" % \
                    (index, len(self.urls), url) 
                ThreadedServiceFetcher.log(message, colorama.Fore.GREEN) 

            except:
                exc_message = traceback.format_exc()
                message = "%s/%s - Scraping %s failed: %s" % \
                    (index, len(self.urls), url, exc_message)
                ThreadedServiceFetcher.log(message, colorama.Fore.MAGENTA)
                # Too many of these? Might need to update scraper method 
                self.data[url] = None
                continue

    def get_data(self):
        return self.data
        

class ThreadedServiceFetcherManager:

    def __load_proxies__(self, path_to_proxies):
        good_proxies = proxy_loader.ProxyLoader.load_proxies(path_to_proxies)
        proxies_to_use = [None, None, None, None, None]
        proxies_to_use.extend(good_proxies)
        return proxies_to_use
    
    def __init__(self, urls, scraper_class, path_to_proxies, headers={}):
        self.scraper_class = scraper_class
        self.proxies = self.__load_proxies__(path_to_proxies)
        self.num_threads = len(self.proxies)
        self.proxies = cycle(self.proxies)

        self.num_to_process = len(urls)

        n = int(self.num_to_process / float(self.num_threads))
        self.groups = [urls[i:i+n] for i in range(0, len(urls), n)]  
             
    def threaded_fetch(self):
        start_time = datetime.datetime.now()
        analyzers = []
        for group in self.groups:
            analyzer = ThreadedServiceFetcher(group, self.proxies.next(),\
                self.scraper_class, 'GET', {}, headers)
            analyzer.setDaemon(True)
            analyzer.start()
            analyzers.append(analyzer)
        for index, analyzer in enumerate(analyzers):
            try:
                analyzer.join()
            except:
                pass

        end_time = datetime.datetime.now()
        seconds_taken = (end_time - start_time).seconds
        num_records_saved = 0

        # Ask each analyzer for its data
        data = [analyzer.get_data() for analyzer in analyzers]
        num_failures = sum([len(filter(lambda x: x is None, datum.values())) for datum in data])
        num_success = sum([len(filter(lambda x: not(x is None), datum.values())) for datum in data])

        return [data, num_failures, num_success]
        
