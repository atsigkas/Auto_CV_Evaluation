from ..google_search import GoogleSearch
from bs4 import BeautifulSoup
from ..utils import *

class Researchgate(GoogleSearch):

    def __init__(self, candidate, website):
        super().__init__(candidate, website)
        self.publication_index = 0

    def search(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        max = 0
        found = False
        max_href = ''
        for link in soup.find_all('a', href=True):
            if "profile" in link['href'] or "scientific-contributions" in link['href']:
                print(f"Name of the Candidate:{self.candidate['name']}")
                print(f"Name in the Publication:{link.text}")
                print(f"the similarity:{similarity(self.candidate['name'].lower(), link.text.lower())}")
                sim = similarity(self.candidate['name'].lower(), link.text.lower())
                if sim > 0.7 and sim > max:
                    max = sim
                    max_href = link['href']
                    found = True
        if max !=0 and found:
            self.candidate['researchgate_url'] = max_href
            print(f"We find the profile of the Author: {self.candidate['name']}.")
        return self.candidate

    def search_author(self, path):
        print('### Research Gate ###')
        author_url = self.candidate['name'].replace(" ", "+")
        paper_url = self.candidate['publications'][self.publication_index]['title'].replace(" ", "+")
        url = "https://www.google.com/search?q="+self.website+'+'+author_url+'+'+paper_url
        response = get_proxy_url(url,True)

        soup = BeautifulSoup(response, "html.parser")
        links = soup.find_all('a', href=True)
        similarity_scores = []
        urls = []

        for link in links:
            url = link['href']
            if path in url:
                url_split = url.split('_', 1)[1]
                print(url)
                print(f"The publication by the PDF:{self.candidate['publications'][self.publication_index]['title']}")
                print(f"The URL splitted:{url_split}")
                print(f"the similarity:{similarity(url_split, self.candidate['publications'][self.publication_index]['title'])}")
                similarity_scores.append(similarity(url_split, self.candidate['publications'][self.publication_index]['title']))
                urls.append(url)

        similarity_table = list(zip(urls, similarity_scores))
        similarity_table.sort(key=lambda x: x[1], reverse=True)

        for url, score in similarity_table:
            if score > 0.7:
                try:
                    response = get_proxy_url(url, True)
                    self.search(response)
                    if self.candidate['researchgate_url'] !='':
                        return
                except Exception as error:
                    print("Unexpected error to find Author.")
                    print(error)

        if self.publication_index < len(self.candidate['publications']):
            self.publication_index += 1
            self.search_author(path)
        return
