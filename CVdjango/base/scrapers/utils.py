from urllib.parse import urlencode
from difflib import SequenceMatcher

'''
API_KEY = '98042e97-cd60-49e0-b01a-12a9debe09c7'
https://proxy.scrapeops.io/v1/?
'''
API_KEY='3e2b034a8797765ba1f14fa1f1f5078b'

def get_proxy_url( url, UsingProxy):
    if UsingProxy is True:
        payload = {'api_key': API_KEY, 'url': url}
        proxy_url = 'http://api.scraperapi.com?' + urlencode(payload)
        return proxy_url
    else:
        return url


def similarity( a, b):
    return SequenceMatcher(None, a, b).ratio()

def extract_text(soup, selector):
    element = soup.select_one(selector)
    if element is not None:
        result = element.text
    else:
        return 'FALSE'

    return result
