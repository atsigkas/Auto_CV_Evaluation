from CVdjango.Sitescrapers.Sitescrapers.spiders.google import GoogleSpider
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

# Set the SCRAPY_SETTINGS_MODULE environment variable

website='site:researchgate.net'
author='Grigorios Tsoumakas'
author2 = author.replace(" ", "+")
paper='Dense Distributions from Sparse Samples: Improved Gibbs Sampling Parameter Estimators for LDA'
paper2=paper.replace(" ", "+")
url = "https://www.google.com/search?q="+website+'+'+author2+'+'+paper2
#url='https://www.researchgate.net/profile/Grigorios-Tsoumakas'

settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(GoogleSpider, start_url=url,author=author,paper=paper)
    #yield runner.crawl(Researchgate, start_url=url,author=author, paper=paper)
    reactor.stop()

crawl()
reactor.run()  # the script will block here until the last crawl call is finished

