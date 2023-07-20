from urllib.parse import urlencode
from difflib import SequenceMatcher


API_KEY = '24431899-a58a-4bbf-adf4-c9331859fd00'


def get_proxy_url( url, UsingProxy):
    if UsingProxy is True:
        payload = {'api_key': API_KEY, 'url': url}
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
        return proxy_url
    else:
        return url


def similarity( a, b):
    return SequenceMatcher(None, a, b).ratio()

def extract_text(soup, selector):
    try:
        element = soup.select_one(selector)
        if element is not None:
            result = element.text
        else:
            raise ValueError(f"No element found with selector '{selector}'.")
    except AttributeError as e:
        print(f"AttributeError encountered: {e}. Unable to extract text.")
        raise
    except Exception as e:
        print(f"Unexpected error encountered: {e}. Unable to extract text.")
        raise
    return result
