import  requests
from bs4 import BeautifulSoup
from .utils import *
from abc import ABC, abstractmethod


class GoogleSearch(ABC):
    def __init__(self, candidate, website):
        self.candidate = candidate
        self.website = website

    @abstractmethod
    def search(self, response):
        pass  # no implementation here

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