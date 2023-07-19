from CVdjango.base.scrapers.search_author_researchgate import GoogleSearch
from bs4 import BeautifulSoup
from CVdjango.base.scrapers.utils import *


class Researchgate(GoogleSearch):

    def __init__(self, candidate, website):
        super().__init__(candidate, website)

    def search(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        found = False
        for link in soup.find_all('a', href=True):
            if "profile" in link['href'] or "scientific-contributions" in link['href']:
                if similarity(self.candidate['author'], link.text) > 0.7 and found is False:
                    found = True
                    self.candidate['researchgate_url'] = link['href']
                    return self.candidate
