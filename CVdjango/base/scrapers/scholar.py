from CVdjango.base.scrapers.google_search import GoogleSearch
from bs4 import BeautifulSoup
from CVdjango.base.scrapers.utils import *
import requests


class Scholar(GoogleSearch):

    def __init__(self, candidate, website):
        super().__init__(candidate, website)

    def search(self, response,url):
        soup = BeautifulSoup(response.text, 'html.parser')
        author = extract_text(soup,'div#gsc_prf_in')
        print(self.candidate['author'],author,similarity(self.candidate['author'], author))
        if similarity(self.candidate['author'], author) > 0.7:
            self.candidate['googlescholar_url'] = url
            return self.candidate

    def get_and_apply(self,url, callback,):
        response = requests.get(get_proxy_url(url, True))
        if response.status_code == 200:
            return callback(response,url)

    def search_author(self, path):
        author_url = self.candidate['author'].replace(" ", "+")
        paper_url = self.candidate['publication'][0]['title'].replace(" ", "+")
        url = "https://www.google.com/search?q="+self.website+'+'+author_url+'+'+paper_url

        response = requests.get(get_proxy_url(url,True))
        webpage_html_content = response.text
        soup = BeautifulSoup(webpage_html_content, "html.parser")
        links = soup.find_all('a', href=True)
        urls = []

        for link in links:
            url = link['href']
            if path in url:
                urls.append(url)
        print(urls)
        for url in urls:
            try:
                self.get_and_apply(url, self.search)
                if self.candidate['googlescholar_url']:
                    return self.candidate
            except Exception as error:
                print("Problem Found Author")
                print(error)
        return None
