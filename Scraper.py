from threaded_service_fetcher import *
class Scraper:
    @staticmethod
    def scrape(urls, scraper_class, path_to_proxies, headers={}):
        tsfm = ThreadedServiceFetcherManager(urls, scraper_class, path_to_proxies, headers)
        return tsfm.threaded_fetch()
