import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import ResearchGate,similarity,get_proxy_url



class Researchgate(scrapy.Spider):
    name = "researchgate"
    allowed_domains = [ "proxy.scrapeops.io", "www.researchgate.net"]

    def __init__(self, start_url=None,paper=None, *args, **kwargs):
        super(Researchgate, self).__init__(*args, **kwargs)
        self.start_point_url = start_url
        self.start_urls = [get_proxy_url(start_url,True)]
        self.paper = paper
        self.meta = {'paper': paper,'start_urls': self.start_urls, 'start_point_url': self.start_point_url}

    def parse(self, response):
        found = False
        xlink = LinkExtractor()
        i=1
        for link in xlink.extract_links(response):
            if "researchgate.net/publication" in link.url:
                print(link.text,similarity(self.meta['paper'], link.text))
                if similarity(self.meta['paper'], link.text) > 0.8:
                    yield response.follow(get_proxy_url(link.url, True),
                                          callback=self.extract_paper)
                    found=True
                    break
        if found is False:
            try:
                i += 1
                next_page_url = get_proxy_url(self.meta['start_point_url']+'/'+str(i),True)
                yield response.follow(next_page_url,
                                      callback=self.parse)
            except Exception as error:
                print(error)
                print("The paper doesn't exist in ResearchGate")

    def extract_paper(self,response):
        print('Search the Paper')
        print('###Search in the ResearchGate###')

        researchgate = ResearchGate()
        researchgate['type']= response.xpath("//*[contains(@class, 'nova-legacy-e-badge nova-legacy-e-badge--color-green nova-legacy-e-badge--display-inline nova-legacy-e-badge--luminosity-high nova-legacy-e-badge--size-l nova-legacy-e-badge--theme-solid nova-legacy-e-badge--radius-m research-detail-header-section__badge')]/text()").get()
        researchgate['year'] = response.xpath("//div[@class='research-detail-header-section__metadata']/div[1]/ul[1]/li[1]/text()").get()
        researchgate['abstract'] = response.xpath("//div[@class='nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-800 research-detail-middle-section__abstract']/text()").get()
        researchgate['title'] = response.xpath("//h1[@class='nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-900 research-detail-header-section__title']/text()").get()
        researchgate['citation'] = response.xpath("//button[1]/div[1]/div[1]/h2[1]/text()").get()
        print("OK")
        yield researchgate


