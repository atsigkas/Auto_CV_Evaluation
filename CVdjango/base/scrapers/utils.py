from urllib.parse import urlencode
from difflib import SequenceMatcher


API_KEY = '  24431899-a58a-4bbf-adf4-c9331859fd00'


def get_proxy_url( url, UsingProxy):
    if UsingProxy is True:
        payload = {'api_key': API_KEY, 'url': url}
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
        return proxy_url
    else:
        return url


def similarity( a, b):
    return SequenceMatcher(None, a, b).ratio()

def extract_text(soup, selector, default=''):
    try:
        result = soup.select_one(selector).text
    except AttributeError:
        result = default
    return result