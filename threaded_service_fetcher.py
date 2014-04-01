"""
Subclass of thread, fetches a list of urls using ServiceFetcher and a specified proxy.
Uses the passed method to scrape data into a hash. Returns a hash(*H1) with the urls fetched as keys and the hash returned by the scraper as value.

   ThreadedServiceFetcher([url1, url2,..], 'proxy_ip:port', scraper_class, path_proxies_zips)

scraper_class must define "scrape"

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
    
    def __init__(self, urls, proxy, scraper_class):
        self.urls = urls
        self.proxy = proxy
        self.data = {}
        self.scraper_class = scraper_class=
        super(ThreadedServiceFetcher, self).__init__()

    def run(self):
        for index, url in enumerate(self.urls):
            try:
                # Fetch the URL using the specified proxy
                sf = service_fetcher.ServiceFetcher(self.proxy)
                response, headers = sf.fetchAsBrowser(url)
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
        pch = proxy_loader.ProxyChecker(path_to_proxies)
        good_proxies = pch.check_proxies('http://www.pinterest.com/ohjoy')
        proxies_to_use = [None, None, None, None, None]
        proxies_to_use.extend(good_proxies)
        return proxies_to_use

    
    def __init__(self, urls, scraper_class, path_to_proxies):
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
                                                  self.scraper_class)
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
        return [analyzer.get_data() for analyzer in analyzers]
