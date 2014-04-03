from Scraper import Scraper
import BeautifulSoup
import service_fetcher
import traceback
import threading
import time
import pdb

class DummyScraperClass:
    @staticmethod
    def is_repin(resp):
        try:
            bs = BeautifulSoup.BeautifulSoup(resp)
            divs_with_class = filter(lambda x: x.has_key('class'), bs.findAll('div'))
            div_credit = filter(lambda h: 'pinnerViaPinnerCredit' in h['class'], divs_with_class)[0]
            all_links = map(lambda h: h['href'], filter(lambda x: x.has_key('href'), div_credit.findAll('a')))
            target_links = filter(lambda x: x.count('/') == 2, all_links)
            user_name = DummyScraperClass.get_owner_username(resp)
            return not(user_name in target_links)
        except:
            print traceback.format_exc()
            return False

    @staticmethod
    def get_owner_username(resp):    
        if resp.__class__.__name__ == 'str':
            bs = BeautifulSoup.BeautifulSoup(resp)
        else:
            bs = resp
        meta = filter(lambda x: 'pinterestapp:pinner' in x['property'], \
                      filter(lambda x: x.has_key('property'), bs.findAll('meta')))[0]
        return meta['content'].replace('http://www.pinterest.com', '')

    @staticmethod
    def scrape(html):
        """
        Scraping code goes here. 
        """
        is_repin = DummyScraperClass.is_repin(html)
        return {'is_repin': is_repin}

class ThreadedAnalyzeRepinRate(threading.Thread):

    def __init__(self, path_to_proxies, profile_url):
        self.path_to_proxies = path_to_proxies
        self.profile_url = profile_url
        self.summary_data = {}
        super(ThreadedAnalyzeRepinRate, self).__init__()
                
    def get_pin_urls(self, resp):
        pin_urls = []
        bs = BeautifulSoup.BeautifulSoup(resp)
        for anchor in filter(lambda x: x.has_key('href'), bs.findAll('a')):
            if anchor['href'].startswith('/pin/'):
                pin_url = anchor['href']
                if not pin_url.startswith('http://'):
                    pin_url = 'http://www.pinterest.com%s' % pin_url
                    
                if not (pin_url.endswith('/repins/') or pin_url.endswith('/likes/')):
                    pin_urls.append(pin_url)
        return list(set(pin_urls))
        
    def run(self):
        headers = {'User-agent': 'Mozilla'}
        resp, hdrs = service_fetcher.ServiceFetcher().fetchURL(self.profile_url)
        pin_urls = self.get_pin_urls(resp)
    
        data, num_failures, num_success = Scraper.scrape(pin_urls, DummyScraperClass, self.path_to_proxies, headers)
        print "%s failures, %s successes" % (num_failures, num_success)

        # Merge result data into a single hash
        for datum in data:
            self.summary_data.update(datum)

        is_repin_values = map(lambda x: x['is_repin'], filter(lambda x: not(x is None), summary_data.values()))
        num_repins = is_repin_values.count(True)
        num_reg_pins = is_repin_values.count(False)
        print "Number pins for %s : %s" % (self.profile_url, len(pin_urls))
        print "   Number repins: %s" % num_repins
        print "   Number regular pins: %s" % num_reg_pins
        print "%% Repins: %s" % (num_repins / float(num_repins + num_reg_pins))

    def get_data(self):
        return self.summary_data

class Timer:    
    def __enter__(self):
        self.start = time.clock()
        return self
    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


def get_multiple_profile_urls_repin_rate(path_to_proxies, user_names):
    profile_urls = []
    for user_name in user_names:
        profile_urls.append('http://www.pinterest.com%spins/' % user_name)
    print profile_urls
    analyzers = []
    for index, profile_url in enumerate(profile_urls):
        print "Starting analyzer %s" % index
        new_analyzer = ThreadedAnalyzeRepinRate(path_to_proxies, profile_url)
        new_analyzer.daemon = True
        new_analyzer.start()
        analyzers.append(new_analyzer)
    
    for analyzer in analyzers:
        analyzer.join()

    # Collect final data from all threads
    global_summary = {}
    for analyzer in analyzers:
        global_summary.update(analyser.get_data())
    return global_summary


if __name__ == '__main__':
    path_to_proxies = raw_input("Path to folder with proxy zip files ") # Run proxy_zip_downloader.py first
    path_to_proxies += "" if path_to_proxies.endswith("/") else "/"

    user_names = ['/sbletnitsky/','/mounthagen/','/Dirty_Chai/','/18asianstars/','/imoveisbahia/','/gearheads01/','/StokerHQHD13/','/zeldivatravels/','/pakes1986/','/fourwaystravels/','/imanilchudasama/','/wiwin2997/','/marciafpantano/','/couturebyayca/','/cookinghawaiian/']
    with Timer() as t:
        data = get_multiple_profile_urls_repin_rate(path_to_proxies, user_names)
        
    print ">> Scraped %s urls in %s" % (len(user_names) * 26, t.interval)
