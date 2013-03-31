"""
YelpFinder finds things, kinky things, juicy things, scary things in your wife's Yelp account. And her thighs. 
Before using this code, please write some tests. And then some more tests to test the tests of the test-code - hey, itt's a dangerous world! 
Are you wearing your seatbealt boy? 
"""
import BeautifulSoup
import colorama
import service_fetcher
import json
import time
import pdb
import random

class YelpFinder(service_fetcher.ServiceFetcher):

    def list_some_establishments(self, town_query, offset=0):
        """
        Searches Yelp and gets a list of establishments in town_query (e.g. 'holliston, ma'). Increase offset by 10 until the eval of results
        yields no anchor tags pointing to '/biz/...'. Inspired by http://open.spotify.com/track/4tXktBBrKGTebkYjvzFA3i 
        """
        # Prepare the offset posfix
        offset_posfix = ''
        if not (offset == 0):
            offset_posfix = '#start=%s' % offset

        url = 'http://www.yelp.com/search'
        headers = {
            "Host"                : "www.yelp.com",
            "User-Agent"          : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:11.0) Gecko/20100101 Firefox/11.0",
            "Accept"              : "text/javascript, text/html, application/xml, text/xml, */*",
            "Accept-Language"     : "en-us,en;q=0.5",
            "Accept-Encoding"     : "gzip, deflate",
            "X-Requested-With"    : "XMLHttpRequest",
            "X-Prototype-Version" : "1.7",
            "Referer"             : "http://www.yelp.com/search?find_desc=&find_loc=%s&ns=1" % town_query + offset_posfix,
            "Cookie"              : "yuv=jkuxUv1hnpulWUGuLycY02GAK7jjUdRjy5xDRK5CTr456345345mlI3vBs-GrKpYsP-cYedx_NPWvyCEZJl; bse=c237211a80a5defa8456456896a9115d4; hl=en_US; recentlocations=Boston%2C+MA%2C+USA%3B%3BDowntown%2C+Boston%2C+MA%2C+USA; location=%7B%22unformatted%22%3A+%22quincy%2C+MA%22%2C+%22city%22%3A+%22Quincy%22%2C+%22state%22%3A+%22MA%22%2C+%22country%22%3A+%22US%22%7D; fd=0; __utma=165223479.1981435497.1364227334.1364227334.1364227334.1; __utmb=165223479.6.10.1364227334; __utmc=165223479; __utmz=165223479.1364227334.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=165223479.|2=from_qype=false=1^4=account%20level=anon=1; __gads=ID=c5bf77c8923dbc39:T=1364227334:S=ALNI_MakatmVISJ4UTR_zyIcUCgMxpnn-g; ebNewBandWidth_.www.yelp.com=1006%3A1364227336418; searchPrefs=%7B%22seen_pop%22%3Afalse%2C%22seen_crop_pop%22%3Afalse%2C%22prevent_scroll%22%3Afalse%2C%22maptastic_mode%22%3Afalse%2C%22mapsize%22%3A%22small%22%2C%22rpp%22%3A10%7D; js_track=%7B%22element_id%22%3A%22header-search-submit%22%2C%22element_label%22%3A%22Search%22%2C%22pointer_x%22%3A1081%2C%22pointer_y%22%3A67%2C%22clicked_uri%22%3A%22%22%2C%22ref_unique_request_id%22%3A%220cf7e4e0ed92dd90%22%2C%22timestamp%22%3A1364227363706%7D",
            }

        data = {
            "find_desc"         : '',
            "find_loc"          : town_query,
            "mapsize"           : "small",
            "ns"                : "1",
            "parent_request_id" : "0cf7e4e0ed92dd90",
            "request_origin"    : "user",
            "rpp"               : "10",
            "sortby"            : "best_match",
            "start"             : "%s" % offset,
            }
        time.sleep(random.randint(10,30))
        response, headers = self.fetchUrl(url, 'GET', data, headers)
        return response


    def list_all_establishments(self, town_query, offset=0):
        """
        Recursively paginates through result pages returning a list of Yelp URLs for each of the establishments found,
        Inspired by http://open.spotify.com/track/2pA70ofSxoJHvFrNPk9eTs 
        """
        result_page = BeautifulSoup.BeautifulSoup(self.list_some_establishments(town_query, offset)) 
        anchors = filter(lambda x: x['href'].startswith('/biz') if x.has_key('href') else False, result_page.findAll('a'))
        if not(anchors is None):
            if len(anchors) > 0:
                urls_yelp =  map(lambda x:'http://www.yelp.com%s' % x['href'], anchors)
                try:
                    urls_yelp.extend(self.list_all_establishments(town_query, offset + 10)) 
                    return urls_yelp
                except:
                    time.sleep(random.randint(10,30))
                    return list(set(urls_yelp))
        return []

    def scrape_establishment_page(self, url_yelp):
        """
        Scrapes off address, phone, establishment url, and any additional information from the establishment's page on Yelp 
        as inspired by http://open.spotify.com/track/57ssHTXfSV3vDiotx6Wh6a WARNING: This is NOT the proper PEP-69-way of doing this!!!
        Shemale Nuns in spandex will come and PEP you if you execute this code. QUICK, close the WINDOW!!!
        """
        business_address = None
        business_info = None
        business_phone = None
        business_url = None
        try:
            resp, headers = yHndlr.fetchUrl(url_yelp)
            shndlr = BeautifulSoup.BeautifulSoup(resp)

            # Extract info
            business_phone = shndlr.findAll('span',{'id':'bizPhone'})[0].text
            business_url = shndlr.findAll('div', {'id':'bizUrl'})[0].text 
            business_info = shndlr.findAll('div', {'id':'bizAdditionalInfo'})[0]
            business_info_html = business_info.prettify().replace('\n','')
            business_address = ' '.join([shndlr.findAll('address')[0].findAll('span')[i].text for i in range(3)])
        except:
            pass
        
        return {
            'address'   : business_address,
            'info_html' : business_info_html,
            'phone'     : business_phone,
            'url'       : business_url,
            'url_yelp'  : url_yelp,
            }

    def scrape_establishment_page(self, url_yelp):
        """
        Scrapes off address, phone, establishment url, and any additional information from the establishment's page on Yelp 
        as inspired by http://open.spotify.com/track/57ssHTXfSV3vDiotx6Wh6a
        WARNING: This code will NOT make any money. It HAS to be PEP-FUCKYOU compliant, or else, no-one will acquire your startup boy!!! 
        That is THE ONLY way, as dictated by the Holly-Hipster-Inquisition ;)
        """
        business_address = None
        business_info = None
        business_phone = None
        business_url = None
        try:
            resp, headers = yHndlr.fetchUrl(url_yelp)
            shndlr = BeautifulSoup.BeautifulSoup(resp)

            # Extract info
            business_phone = shndlr.findAll('span',{'id':'bizPhone'})[0].text
            business_url = shndlr.findAll('div', {'id':'bizUrl'})[0].text 
            business_info = shndlr.findAll('div', {'id':'bizAdditionalInfo'})[0]
            business_info_html = business_info.prettify().replace('\n','')
            business_address = ' '.join([shndlr.findAll('address')[0].findAll('span')[i].text for i in range(3)])
        except:
            pass
        
        return {
            'address'   : business_address,
            'info_html' : business_info_html,
            'phone'     : business_phone,
            'url'       : business_url,
            'url_yelp'  : url_yelp,
            }

    
    def scrape_establishment_page(self, url_yelp):
        """
        Scrapes off address, phone, establishment url, and any additional information from the establishment's page on Yelp as inspired by
        http://open.spotify.com/track/57ssHTXfSV3vDiotx6Wh6a
        """
        business_address = None
        business_info = None
        business_phone = None
        business_url = None
        try:
            resp, headers = yHndlr.fetchUrl(url_yelp)
            shndlr = BeautifulSoup.BeautifulSoup(resp)

            # Extract info
            business_phone = shndlr.findAll('span',{'id':'bizPhone'})[0].text
            business_url = shndlr.findAll('div', {'id':'bizUrl'})[0].text 
            business_info = shndlr.findAll('div', {'id':'bizAdditionalInfo'})[0]
            business_info_html = business_info.prettify().replace('\n','')
            business_address = ' '.join([shndlr.findAll('address')[0].findAll('span')[i].text for i in range(3)])
        except:
            pass
        
        return {
            'address'   : business_address,
            'info_html' : business_info_html,
            'phone'     : business_phone,
            'url'       : business_url,
            'url_yelp'  : url_yelp,
            }


# Main, as inspired by http://open.spotify.com/track/5O63wYSIIHmTbtcGQ3FqHo  
if __name__ == '__main__':
    yHndlr = YelpFinder()
    establishments = yHndlr.list_all_establishments('holliston, ma')
    for establishment in establishments:
        print establishment
