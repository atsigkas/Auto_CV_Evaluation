from CVdjango.base.scrapers.search_author_researchgate import GoogleSearch
from bs4 import BeautifulSoup
from CVdjango.base.scrapers.utils import *


class Scholar(GoogleSearch):

    def __init__(self, candidate, website):
        super().__init__(candidate, website)

    def search(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        author = extract_text(soup, 'googlescholar_url', 'div#gsc_prf_in')
        print("OK")
        if similarity(self.candidate['author'], author) > 0.7 :
            self.candidate['googlescholar_url'] = response.request.url
            return self.candidate
