"""
ThreadedChecker   Tries fetching a URL using a specified proxy. 'Good proxies' get added to good_proxies_db
                  When 'check_relative' is set, attempts fetching a different page via the same proxy, one that is
                  expected not to have blocked the proxy. This is done to check if the domain PROXY_CHECK_URL_A is 
                  is explicitly blocking the proxy or not (403s)
ProxyChecker      Opens a hidemyass zip file of proxies, and runs ThreadedChecker on each of them (~900 threads).
                  The good_proxies_db file handler gets passed to each ThreadedChecker to store in the text file the
                  'good proxies.'
"""
import colorama
import service_fetcher
import threading
import urllib2
import zipfile

class ThreadedChecker(threading.Thread):

    PROXY_CHECK_URL_A = 'http://www.yelp.com/holliston-ma-us'
    PROXY_CHECK_URL_B = 'http://www.prensalibre.com'
    
    def __init__(self, proxy, check_relative, good_proxies_db):
        self.proxy = proxy
        self.check_relative = check_relative
        self.good_proxies_db = good_proxies_db
        super(ThreadedChecker, self).__init__()

    def run(self):

        fetcher = service_fetcher.ServiceFetcher(self.proxy)
        error_a = ''
        error_b = ''

        try:
            response, headers = fetcher.fetchUrl(ThreadedChecker.PROXY_CHECK_URL_A) 
        except urllib2.HTTPError, e:
            error_a = '%s' % e.code
        except:
            error_a = 'connection refused'
            
        if self.check_relative:
            try:
                response, headers = fetcher.fetchUrl(ThreadedChecker.PROXY_CHECK_URL_B) 
            except urllib2.HTTPError, e:
                error_b = '%s' % e.code
            except:
                error_b = 'connection refused'

            if len(error_a) == 0 and len(error_b) == 0:
                print colorama.Fore.GREEN + self.proxy
                self.good_proxies_db.write(self.proxy + '\n')
            else:
                if error_a == error_b:
                    print colorama.Fore.RED + '%s: Down' % self.proxy
                else:
                    print colorama.Fore.MAGENTA + '%s: Yelp(%s) vs Prensalibre(%s)' % (proxy, error_a, error_b)
        else:
            if len(error_a) == 0:
                print colorama.Fore.GREEN + self.proxy + colorama.Fore.WHITE
                self.good_proxies_db.write(self.proxy + '\n')
            else:
                print colorama.Fore.RED + self.proxy + colorama.Fore.WHITE
                

class ProxyChecker:

    def __init__(self, path_to_zip='/Users/yomama/Downloads/proxylist-03-11-13.zip'):
        zfile = zipfile.ZipFile(path_to_zip)
        proxies_list = zfile.read('full_list_nopl/_reliable_list.txt')
        self.proxies = proxies_list.replace('\r','').split('\n')
        print colorama.Fore.YELLOW + '%s proxies loaded' % len(self.proxies) + colorama.Fore.WHITE

    def check_proxies(self, check_relative=True):
        threaded_checkers = []
        good_proxies_db = open('good_proxies.db', 'w') # fuck the db. Don't have time for pretty schemas in pink.
        for proxy in self.proxies:
            checker = ThreadedChecker(proxy, check_relative, good_proxies_db)
            checker.start()
            threaded_checkers.append(checker)
        for checker in threaded_checkers:
            checker.join()
        print colorama.Fore.WHITE + 'Done'
        good_proxies_db.close()


if __name__ == '__main__':
    pchecker = ProxyChecker()
    good_proxies = pchecker.check_proxies(False)
    
