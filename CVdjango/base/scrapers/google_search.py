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

    @abstractmethod
    def search_author(self, path):
        pass

    def update_candidate(self, col, field):
        try:
            result = col.update_one(
                {"_id": self.candidate['_id']},
                {"$set": {field: self.candidate[field]}}
            )
        except Exception as e:
            print(f"An error occurred when updating the document: {e}")
