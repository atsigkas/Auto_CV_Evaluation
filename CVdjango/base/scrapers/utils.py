from urllib.parse import urlencode
from difflib import SequenceMatcher


API_KEY = '7335ee33-d1e8-4a2a-9166-672f20fcaece'


def get_proxy_url( url, UsingProxy):
    if UsingProxy is True:
        payload = {'api_key': API_KEY, 'url': url}
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
        return proxy_url
    else:
        return url


def similarity( a, b):
    return SequenceMatcher(None, a, b).ratio()