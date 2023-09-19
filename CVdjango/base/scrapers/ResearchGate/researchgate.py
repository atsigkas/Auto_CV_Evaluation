from ..google_search import GoogleSearch
from bs4 import BeautifulSoup
from ..utils import *
import requests

class Researchgate(GoogleSearch):

    def __init__(self, candidate, website):
        super().__init__(candidate, website)
        self.publication_index = 0

    def search(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        found = False
        for link in soup.find_all('a', href=True):
            if "profile" in link['href'] or "scientific-contributions" in link['href']:
                print(f"Name of the Candidate:{self.candidate['author']}")
                print(f"Name in the Publication:{link.text}")
                print(f"the similarity:{similarity(self.candidate['author'], link.text)}")
                if similarity(self.candidate['author'], link.text) > 0.7 and found is False:
                    found = True
                    #cleaned_url = link['href'].replace("\"", "").replace("\\", "")
                    self.candidate['researchgate_url'] = link['href']
                    print(f"We find the profile of the Author: {self.candidate['author']} . This is the name in the publication {link.text}")
                    return self.candidate

    def search_author(self, path):
        print('### Research Gate ###')
        author_url = self.candidate['author'].replace(" ", "+")
        paper_url = self.candidate['publication'][self.publication_index]['title'].replace(" ", "+")
        url = "https://www.google.com/search?q="+self.website+'+'+author_url+'+'+paper_url
        response = get_proxy_url(url,True)

        #webpage_html_content = response.text
        soup = BeautifulSoup(response, "html.parser")
        links = soup.find_all('a', href=True)
        similarity_scores = []
        urls = []

        for link in links:
            url = link['href']
            if path in url:
                url_split = url.split('_', 1)[1]
                print(url)
                print(f"The publication by the PDF:{self.candidate['publication'][self.publication_index]['title']}")
                print(f"The URL splitted:{url_split}")
                print(f"the similarity:{similarity(url_split, self.candidate['publication'][self.publication_index]['title'])}")
                similarity_scores.append(similarity(url_split, self.candidate['publication'][self.publication_index]['title']))
                #cleaned_url = url.replace("\"", "").replace("\\", "")
                urls.append(url)

        similarity_table = list(zip(urls, similarity_scores))
        similarity_table.sort(key=lambda x: x[1], reverse=True)

        for url, score in similarity_table:
            if score > 0.7:
                try:
                    response = get_proxy_url(url, True)
                    self.search(response)
                    # self.get_and_apply(url, self.search)
                    return
                except Exception as error:
                    print("Unexpected error to find Author.")
                    print(error)

        if self.publication_index < len(self.candidate['publication']):
            self.publication_index += 1
            self.search_author(path)
        return
