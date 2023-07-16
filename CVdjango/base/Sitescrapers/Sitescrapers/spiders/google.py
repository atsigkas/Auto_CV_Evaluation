import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import SiteItem,similarity,get_proxy_url


def search(response):
    xlink = LinkExtractor()
    for link in xlink.extract_links(response):
        try:
            if "researchgate.net/publication" in link.url or "www.researchgate.net/scientific-contributions" in link.url:
                url_split= link.url.split('/', 4)[4]
                if similarity(response.meta['author'],url_split)>0.3:
                    response.meta['site_item'][response.meta['site']] = link.url
                    yield response.meta['site_item']
                else:
                    yield None
        except Exception as error:
            print(error)
            print("In the paper we couldn't find the name of the candidate")


class GoogleSpider(scrapy.Spider):
    name = "researchgate"
    allowed_domains = ["google.com", "proxy.scrapeops.io", "www.researchgate.net", "semanticscholar.org"]

    def __init__(self, start_url=None, author=None, paper=None, *args, **kwargs):
        super(GoogleSpider, self).__init__(*args, **kwargs)
        proxy_url = get_proxy_url(start_url, True)
        self.start_urls = [proxy_url]
        self.author = author
        self.paper = paper
        self.meta = {'author': author, 'paper': paper}

    def parse(self, response):
        print('Search the Author')
        print('###Search in the google###')
        site_item = SiteItem()
        site_item['researchgate_url'] = None
        similarity_scores = []
        urls = []

        xlink = LinkExtractor()
        for link in xlink.extract_links(response):
            if "researchgate.net/publication" in link.url:
                print('### Find ResearchGate ###')
                url_split= link.url.split('_', 1)[1]
                similarity_scores.append(similarity(url_split, self.meta['paper']))
                urls.append(link.url)

        similarity_table = list(zip(urls, similarity_scores))
        similarity_table.sort(key=lambda x: x[1], reverse=True)
        print(similarity_table)
        for url, score in similarity_table:
            if score >0.8:
                yield response.follow(get_proxy_url(url, True),
                                      callback=search,
                                      meta={'site_item': site_item,
                                            'author': self.meta['author'],
                                            'site': 'researchgate_url'})