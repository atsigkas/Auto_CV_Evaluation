import  requests
from bs4 import BeautifulSoup
from CVdjango.base.scrapers.utils import *
from abc import ABC, abstractmethod


class GoogleSearch(ABC):
    def __init__(self, candidate, website):
        self.candidate = candidate
        self.website = website

    @abstractmethod
    def search(self, response):
        pass  # no implementation here

    def get_and_apply(self, url, callback):
        response = requests.get(get_proxy_url(url, True))
        if response.status_code == 200:
            return callback(response)

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
                similarity_scores.append(similarity(url_split, self.candidate['publication'][0]['title']))
                urls.append(url)

        similarity_table = list(zip(urls, similarity_scores))
        similarity_table.sort(key=lambda x: x[1], reverse=True)
        print(similarity_table)
        for url, score in similarity_table:
            if score > 0.8:
                try:
                    self.get_and_apply(url, self.search)
                    return self.candidate
                except Exception as error:
                    print("Problem Found Author")
                    print(error)
        return None

    def update_candidate(self, col, field):
        result = col.update_one(
            {"_id": self.candidate['_id']},
            # Update: researchgate_url
            {"$set": {field: self.candidate[field]}}
        )
