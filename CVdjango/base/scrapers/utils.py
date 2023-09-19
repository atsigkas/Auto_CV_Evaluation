from urllib.parse import urlencode
from difflib import SequenceMatcher
import requests



'''
API_KEY = '98042e97-cd60-49e0-b01a-12a9debe09c7'
https://proxy.scrapeops.io/v1/?
'''

# scraperapi
API_KEY='3e2b034a8797765ba1f14fa1f1f5078b'

# flaresolverr
FLARESOLVERR=True
SCRAAPERAPI=False
SCRAPEOPS=False

def get_data(url,UsingProxy):
    if FLARESOLVERR:
        post_body = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": 60000
        }
        response = requests.post('http://localhost:8191/v1', headers={'Content-Type': 'application/json'}, json=post_body)
        response_json = response.json()
        webpage_html_content = response_json["solution"]["response"]
        return webpage_html_content


def get_proxy_url( url, UsingProxy):
    if SCRAAPERAPI or SCRAPEOPS:
        if UsingProxy is True:
            payload = {'api_key': API_KEY, 'url': url}
            proxy_url = 'http://api.scraperapi.com?' + urlencode(payload)
            response = requests.post(url)
            return response
    elif FLARESOLVERR:
        return get_data(url, UsingProxy)
    else:
        print("Enable Proxy")


def similarity( a, b):
    return SequenceMatcher(None, a, b).ratio()

def extract_text(soup, selector):
    element = soup.select_one(selector)
    if element is not None:
        result = element.text
    else:
        return ''

    return result
