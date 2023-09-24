from ..google_search import GoogleSearch
from bs4 import BeautifulSoup
from ..utils import *
import requests
from scholarly import scholarly
from urllib.parse import urlparse, parse_qs
import json


def extract_scholar_id( url):
    try:
        # Parse the URL
        parsed_url = urlparse(url)

        # Parse the query string
        query_string = parse_qs(parsed_url.query)

        # Get the author ID
        author_id = query_string['user'][0]
    except Exception as e:
        print(f"Error to extract author id this url: '{url}'")
        print(f"Error:{e}")

    return author_id


class Scholar(GoogleSearch):

    def __init__(self, candidate, website):
        super().__init__(candidate, website)
        self.publication_index=0



    def search(self, response,url):
        soup = BeautifulSoup(response, 'html.parser')
        author = extract_text(soup,'div#gsc_prf_in')
        print(self.candidate['author'].lower(), author.lower(), similarity(self.candidate['author'].lower(), author.lower()))
        if similarity(self.candidate['author'].lower(), author.lower()) > 0.7:
            author_id=extract_scholar_id(url)
            try:
                author = scholarly.search_author_id(author_id)
                author_filled = scholarly.fill(author, sections=["publications"])
            except Exception:
                print(f"Error to find search_query : '{author}'")
            print(json.dumps(author_filled, indent=4))
            for publication in author_filled["publications"]:
                print(publication["bib"]["title"])
                print(self.candidate['publication'][self.publication_index]['title'])
                if similarity(self.candidate['publication'][self.publication_index]['title'], publication["bib"]["title"]):
                    self.candidate['googlescholar_url'] = url
                    return self.candidate


    def get_and_apply(self,url, callback):
        response = requests.get(get_proxy_url(url, True))
        if response.status_code == 200:
            return callback(response,url)

    def search_author(self, path):
        author_url = self.candidate['author'].lower().replace(" ", "+")
        paper_url = self.candidate['publication'][self.publication_index]['title'].replace(" ", "+")
        url = "https://www.google.com/search?q="+self.website+'+'+author_url

        response = get_proxy_url(url,True)
        soup = BeautifulSoup(response, "html.parser")
        links = soup.find_all('a', href=True)
        urls = []

        for link in links:
            url = link['href']
            if path in url:
                urls.append(url)

        for url in urls:
            try:
                response=get_proxy_url(url,True)
                self.search(response,url)
                if self.candidate['googlescholar_url']:
                    return self.candidate
            except Exception as error:
                print("Problem Found Author")
        if self.publication_index < len(self.candidate['publication']):
            self.publication_index += 1
            self.search_author(path)
        return
