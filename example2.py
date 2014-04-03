"""
Example #2 

Given a Pinterest username, scrape the latest 25 pins via ServiceFetcher (single thread), then pass the urls 
to Scraper (25 threads, 25 proxies) and identify repins from non-repins. 
http://www.forentrepreneurs.com/lessons-learnt-viral-marketing/

"""

from Scraper import Scraper
import BeautifulSoup
import service_fetcher
import traceback
import time
import pdb

def get_pin_urls(resp):
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


def get_profile_urls_repin_rate(path_to_proxies, profile_url):
    headers = {'User-agent': 'Mozilla'}
    resp, hdrs = service_fetcher.ServiceFetcher().fetchURL(profile_url)
    pin_urls = get_pin_urls(resp)
    
    data, num_failures, num_success = Scraper.scrape(pin_urls, DummyScraperClass, path_to_proxies, headers)
    print "%s failures, %s successes" % (num_failures, num_success)

    # Merge result data into a single hash
    summary_data = {} 
    for datum in data:
        summary_data.update(datum)

    is_repin_values = map(lambda x: x['is_repin'], filter(lambda x: not(x is None), summary_data.values()))
    num_repins = is_repin_values.count(True)
    num_reg_pins = is_repin_values.count(False)
    print "Number pins for %s : %s" % (profile_url, len(pin_urls))
    print "   Number repins: %s" % num_repins
    print "   Number regular pins: %s" % num_reg_pins
    print "%% Repins: %s" % (num_repins / float(num_repins + num_reg_pins))


if __name__ == '__main__':
    path_to_proxies = raw_input("Abs path to folder with proxy zip files ") # Run proxy_zip_downloader.py first
    path_to_proxies += "" if path_to_proxies.endswith("/") else "/"
    get_profile_urls_repin_rate(path_to_proxies, 'http://www.pinterest.com/mmenchu/pins/')
