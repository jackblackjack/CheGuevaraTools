"""
PostwireFetcher provides the means to post URLS to a specified collection on my account (mmenchu@gmail.com) on Postwire. 
To post to collection under other accounts just replace cookie['session'] and call  post( url, colletionId):
PostwireThreadedFetcher is a simple Thread that creates a PostwireFetcher object and posts 5 urls to the specified board.
It's used in __main__ to post Postwire using multiple threads. 
"""

import colorama
import random
import service_fetcher
import threading
import urllib

class PostwireFetcher(service_fetcher.ServiceFetcher):

    HEADERS = {
        'Host'              : 'www.postwire.com',
        'User-Agent'        : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept'            : '*/*',
        'Accept-Language'   : 'en-us,en;q=0.5',
        'Accept-Encoding'   : 'gzip, deflate',
        'Connection'        : 'keep-alive',
        'X-Requested-With'  : 'XMLHttpRequest',
        'Referer'           : 'https://www.postwire.com/col/516c2b231c675a02e8000069/edit',
        'Cookie'            : '',
        'Pragma'            : 'no-cache',
        'Cache-Control'     : 'no-cache',
        'Content-Length'    : '0',}

    COOKIE = {
        'SnapABugRef'         : 'https%3A%2F%2Fwww.postwire.com%2F%20',
        'SnapABugHistory'     : '12#',
        'optimizelySegments'  : '%7B%7D',
        'optimizelyEndUserId' : '[REMOVED]',
        'optimizelyBuckets'   : '%7B%22207910778%22%3A%22207922354%22%7D',
        '__utma'              : '196702125.1630630043.1366043254.1366043254.1366047468.2',
        '__utmz'              : '196702125.1366043254.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'session'             : 'bFlLWOoFFGSurmW5J5BXILTci4g=?_expires=STEzNjg3MjE2NjYKLg==&_permanent=STAxCi4=&unique_id=Uyc1MTZjMjljMzA5ZWUyNjAyZTkwMDAwN2EnCnAxCi4=&username=Vm1tZW5jaHVAZ21haWwuY29tCnAxCi4=',
        '__utmb'              : '196702125.5.10.1366047468',
        'pw_token'            : '[REMOVED]',
        'AWSELB'              : 'A5A567A91A1FBF725A41076064FB8285F513451DA894ED3C53BBE886CC281C410293CA88835A19C2D809028E0924244AF176C079F2C692C7BFE2A67193AF69FD6E912C6901',
        'SnapABugVisit'       : '6cb7fa04-ab54-4b7b-9eed-3c19a46213f6-668565978363573',
        '__utmc'              : '196702125',
        'mp_370d2f8a22ee8dd22385d29df320bc75_mixpanel' : '%7B%22distinct_id%22%3A%20%2213e0e85dd3b11a-0db6f1359938b88-43662342-fa000-13e0e85dd3d1bc%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
        }


    URL_POST_ITEM = 'https://www.postwire.com/res/item'
    URL_GET_AWSELB_SESSION = 'https://www.postwire.com/messages'

    def __init__(self):
        """
        Constructor. Fetches a new session cookie, if a new one exists. (Not sure this is needed)
        """
        self.pw_token = 'dc866ff0938540f3ad324790fce48a68'
        cookie = PostwireFetcher.COOKIE
        cookie['pw_token'] = self.pw_token
        headers = PostwireFetcher.HEADERS
        headers['Cookie'] = '; '.join(['%s=%s' % (key, cookie[key]) for key in cookie.keys()])
        headers['Content-Length'] = '0'
        resp, headers = self.fetchUrl(PostwireFetcher.URL_GET_AWSELB_SESSION, 'GET', {}, headers)
        service_fetcher.ServiceFetcher.__init__(self)
        

    def post(self, url, colletionId):
        data = {
            'collectionId' : colletionId,
            'created'      : "2013-04-15T16:54:26.284Z",
            'image_url'    : "/static/img/loader.gif",
            'mode'         : "edit",
            'title'        : "Analyzing",
            'url'          : url, }

        cookie = PostwireFetcher.COOKIE
        cookie['pw_token'] = self.pw_token
        headers = PostwireFetcher.HEADERS
        headers['Cookie'] = '; '.join(['%s=%s' % (key, cookie[key]) for key in cookie.keys()])
        headers['Content-Length'] = len(urllib.urlencode(data))
        return self.fetchUrl(PostwireFetcher.URL_POST_ITEM, 'POST', data, headers)


class PostwireThreadedFetcher(threading.Thread):

    def __init__(self, pin_urls):
        self.pin_urls = pin_urls
        super(PostwireThreadedFetcher, self).__init__()

    def run(self):
        pwfetcher = PostwireFetcher() 
        for pin_url in self.pin_urls:
            for index, pin_url in enumerate(pin_urls):
                resp, headers = pwfetcher.post(pin_url, "516c2b231c675a02e8000069")
                print colorama.Fore.YELLOW + '%s/%s %s' % (index, len(pin_urls) ,pin_url) + colorama.Fore.WHITE


if __name__ == '__main__':

    pin_urls = open('pin_urls.txt', 'r').readlines()
    url_groups = list(chunks(pin_urls, 5))
 
    threadedFetchers = []
    for index, url_group in enumerate(url_groups):
        ftchr = PostwireThreadedFetcher(url_group)
        ftchr.start()
        threadedFetchers.append(ftchr)
    for ftchr in threadedFetchers:
        ftchr.join()




"""
Sample response after posing a URL

{'content-length': '974', 'set-cookie': {' Path': '/', 'pw_token': '[REMOVED]', ' HttpOnly': ''}, 'server': 'Apache/2.2.20 (Ubuntu)', 'connection': 'Close', 'cache-control': 'no-cache', 'date': 'Mon, 15 Apr 2013 18:51:46 GMT', 'access-control-allow-origin': 'http://www.postwire.com', 'content-type': 'application/json'}
{
  "status": {
    "progress": null,
    "message": "Ready",
    "state": "READY",
    "job_id": null,
    "error_msg": null
  },
  "title": "",
  "file_type": null,
  "type": "ContentItem",
  "created": [REMOVED],
  "image_zoom": "cover",
  "source_url": "[REMOVED]",
  "image_url": "https://d1px4aefz9os8f.cloudfront.net/static/img/icon_pdf.png",
  "image_choices": [],
  "creator": {
    "username": "mmenchu@gmail.com",
    "bio": null,
    "verified": false,
    "sourced_via": null,
    "company_logo": null,
    "image": "https://www.gravatar.com/avatar/1f2117bb72c0c24641e8114faaa69af2?s=150&d=https%3A%2F%2Fd1px4aefz9os8f.cloudfront.net%2Fstatic%2Fimg%2Fdefault_user_image.jpg",
    "email": "mmenchu@gmail.com",
    "phone": null,
    "created_on": [REMOVED],
    "full_name": "Miguel Menchu",
    "company": null,
    "id": "[REMOVED]",
    "job_title": null
  },
  "id": "REMOVED"
"""
