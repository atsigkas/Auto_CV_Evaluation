from CVdjango.base.Sitescrapers.Sitescrapers.spiders.google import GoogleSpider
from CVdjango.base.Sitescrapers.Sitescrapers.spiders.researchgate import Researchgate
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

website='site:researchgate.net'
author='Albie van Dijk'
author = author.replace(" ", "+")
paper='Double‐stranded RNA Viruses'
paper=paper.replace(" ", "+")
url = "https://www.google.com/search?q="+website+'+'+author+'+'+paper
url='https://www.researchgate.net/publication/351196285_Double-stranded_RNA_Viruses'
url='https://www.researchgate.net/scientific-contributions/Albie-VAN-DIJK-2193911786'

settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)

@defer.inlineCallbacks
def crawl():
    #yield runner.crawl(GoogleSpider, start_url=url,author=author,paper=paper)
    yield runner.crawl(Researchgate, start_url=url, paper=paper)
    reactor.stop()

crawl()
reactor.run()  # the script will block here until the last crawl call is finished

