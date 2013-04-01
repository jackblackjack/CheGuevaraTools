"""
ProxyChecker opens a zipfile with a list of proxies (~900) then hits a "private" URL using each of the proxies
to filter out those that are down. The "private" url is nothing but a version of http://wtfismyip.com/ (django)

def knockknock(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return HttpResponse(ip)

"""
import colorama
import service_fetcher
import zipfile

class ProxyChecker:

    PROXY_CHECK_URL = 'http://vivalarevoluciondel3deoctubredondeloscabronesfanaticosdepep8fueronpateadosenelculopornopreocuparseporcosasmasimportantes.com/knockknock'

    def __init__(self, path_to_zip='/Users/mmenchu/Downloads/Porn/Milfs/ContentForIdiotsWhoThinkThisFolderActuallyExists/proxylist-03-11-13.zip'):
        zfile = zipfile.ZipFile(path_to_zip)
        proxies_list = zfile.read('full_list_nopl/_reliable_list.txt')
        self.proxies = proxies_list.replace('\r','').split('\n')
        print colorama.Fore.YELLOW + '%s proxies loaded' % len(self.proxies) + colorama.Fore.WHITE

    def check_proxies(self):
        good_proxies = []
        bad_proxies = []
        for proxy in self.proxies:
            fetcher = service_fetcher.ServiceFetcher(proxy)
            try:
                response, headers = fetcher.fetchUrl(ProxyChecker.PROXY_CHECK_URL) 
                # Response will be something like "20.60.159.151", proxy "20.60.159.151:8080" 
                if response in proxy: 
                    good_proxies.append(proxy)
                    print colorama.Fore.GREEN + proxy
                else:
                    bad_proxies.append(proxy)
                    print colorama.Fore.RED + proxy
            except:
                bad_proxies.append(proxy)
                print colorama.Fore.RED + proxy
                pass

        message = '%s Proxies checked: %s are good, %s are taking a dump ATM.' % (len(self.proxies), len(good_proxies), len(bad_proxies)) 
        print colorama.Fore.MAGENTA + message + colorama.Fore.WHITE
        return good_proxies

if __name__ == '__main__':
    pchecker = ProxyChecker()
    good_proxies = pchecker.check_proxies()
    
