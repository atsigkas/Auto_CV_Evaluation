from CVdjango.base.scrapers.google_search import GoogleSearch
from bs4 import BeautifulSoup
from CVdjango.base.scrapers.utils import *
import requests

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

    def search_author(self, path):
        author_url = self.candidate['author'].replace(" ", "+")
        paper_url = self.candidate['publication'][0]['title'].replace(" ", "+")
        url = "https://www.google.com/search?q="+self.website+'+'+author_url+'+'+paper_url

        response = requests.get(get_proxy_url(url,True))
        webpage_html_content = response.text
        soup = BeautifulSoup(webpage_html_content, "html.parser")
        links = soup.find_all('a', href=True)
        similarity_scores = []
        urls = []

        for link in links:
            url = link['href']
            if path in url:
                url_split = url.split('_', 1)[1]
                print(url_split,similarity(url_split, self.candidate['publication'][0]['title']))
                similarity_scores.append(similarity(url_split, self.candidate['publication'][0]['title']))
                urls.append(url)

        similarity_table = list(zip(urls, similarity_scores))
        similarity_table.sort(key=lambda x: x[1], reverse=True)
        print(similarity_table)
        for url, score in similarity_table:
            if score > 0.7:
                try:
                    self.get_and_apply(url, self.search)
                    return self.candidate
                except Exception as error:
                    print("Problem Found Author")
                    print(error)
        return None
