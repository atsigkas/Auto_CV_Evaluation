# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from urllib.parse import urlencode
from difflib import SequenceMatcher

API_KEY = '7335ee33-d1e8-4a2a-9166-672f20fcaece'

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def get_proxy_url(url,UsingProxy):
    if UsingProxy is True:
        payload = {'api_key': API_KEY, 'url': url}
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
        return proxy_url
    else:
        return url


class SitescrapersItem(scrapy.Item):
    pass


class SiteItem(scrapy.Item):
    author = scrapy.Field()
    paper = scrapy.Field()
    researchgate_id = scrapy.Field()
    researchgate_url = scrapy.Field()

class ResearchGate(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
    abstract = scrapy.Field()
    citation = scrapy.Field()
    topics = scrapy.Field()
    type = scrapy.Field()