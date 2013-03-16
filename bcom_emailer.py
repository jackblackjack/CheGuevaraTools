"""
Boston.com lets people share articles via email. Outgoing emails are handled through their mailservers.
BComEmailer sends a dummy article to a to_email address. Emails containing Non-boston.com URLS seems to get ignored. Wonder why ;) 
"""
import colorama
import service_fetcher
import random
import urllib

class BComEmailer(service_fetcher.ServiceFetcher):
    
    def __init__(self):
        self.url = 'http://www.boston.com/emtaf/'
        
    def send_email(self, to_email, from_email):
        data = {
            'sender_name'      : '',
            'sender_email'     : from_email,
            'recipient_email'  : to_email,
            'message'          : random.choice(['This is so interesting', 'Thought about you babe', 'Read this OMG!!!', "Thought i'd share", 'Here it goes honey']),
            'story_url'        : 'http://www.boston.com/business/healthcare/2013/03/14/fda-probes-new-pancreas-risks-with-diabetes-drugs/ibY7Jr4mWy9dX6hUFpDk2I/story.html',
            }    
        contentLength = len(urllib.urlencode(data))
        headers = {
            'Host'             : 'www.boston.com',
            'User-Agent'       : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:11.0) Gecko/20100101 Firefox/11.0',
            'Accept'           : '*/*',
            'Accept-Language'  : 'en-us,en;q=0.5',
            'Accept-Encoding'  : 'gzip, deflate',
            'Content-Type    ' : 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With' : 'XMLHttpRequest',
            'Referer'          : 'http://www.boston.com/business/healthcare/2013/03/14/fda-probes-new-pancreas-risks-with-diabetes-drugs/ibY7Jr4mWy9dX6hUFpDk2I/story.html',
            'Content-Length'   : '%s' % contentLength,
            'Cookie'           : 'bcpage=6; OAX=QIPkZFBMaj4AC6xs; grvinsights=da4f562e6f1e14cc399be24c7f540c78; s_vi=[CS]v1|2826352085160861-60000198C00056F7[CE]; SS_ARE_Override.traceLevel=WARN; acudeoSession.4c4e038c4eb29=%7B%22time%22%3A1347185220934%7D; __vrf=1363353590629D12bCLJRtG7RiccxIZOX9l37ERPvG0M4; __vru=http%3A//www.boston.com/business/healthcare/2013/03/14/fda-probes-new-pancreas-risks-with-diabetes-drugs/ibY7Jr4mWy9dX6hUFpDk2I/story.html; ssbusi=1; RMFD=011UGUY7O20668s; s_pv=Business%20%7C%20Healthcare%20%7C%20FDA%20probes%20new%20pancreas%20risks%20with%20diabetes%20drugs; __unam=b6206f2-13d6e350a99-26042fec-3; _chartbeat2=j12xn3aknjvtdhhv.1363353604077.1363353817970.00000000000001; JSESSIONID=60D2CD239C300EF112B425A7D26A92F4; pathUrl=http://www.boston.com/business/healthcare/2013/03/14/fda-probes-new-pancreas-risks-with-diabetes-drugs/ibY7Jr4mWy9dX6hUFpDk2I/story.html; pathCnt=1; s_cc=true; s_ppv=21; s_sq=nytbglobe%2Cnytbgglobal%3D%2526pid%253DBusiness%252520%25257C%252520Healthcare%252520%25257C%252520FDA%252520probes%252520new%252520pancreas%252520risks%252520with%252520diabetes%252520drugs%2526pidt%253D1%2526oid%253Djavascript%25253Avoid(0)%2526ot%253DA; __vrm=474_633_1265',
            'Pragma'           : 'no-cache',
            'Cache-Control'    : 'no-cache',
            }
        text, headers = self.fetchUrl(self.url, 'POST', data, headers)
        return text, headers

if __name__ == '__main__':
    bcom = BComEmailer()
    text, headers = bcom.send_email('camiloCienfuegos@mail.ru', 'jhoover@woosyboy.com')                                                                                                        
    #print colorama.Fore.YELLOW + "Text: %s" % text
    #print colorama.Fore.GREEN + "Headers: %s" % headers
    print colorama.Fore.MAGENTA + 'Sent!' if ('success' in text.lower()) else 'Something went wrong!' + colorama.Fore.WHITE
