'''
Pairnw to profile apo api
kai meta varaw gia ka8e publication api
'''
from urllib.parse import urlparse, parse_qs
from scholarly import scholarly
from CVdjango.base.scrapers.utils import *
import requests

def extract_scholar_id(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Parse the query string
    query_string = parse_qs(parsed_url.query)

    # Get the author ID
    author_id = query_string['user'][0]

    return author_id

class ResearchGateScraper:
    def __init__(self, candinate):
        self.candidate=candinate
        self.scholar_publications = []


def check_papers(self):
    # search by unique author id
    author_id = extract_scholar_id('https://scholar.google.com/citations?user=kJBcnigAAAAJ&hl=en')
    author = scholarly.search_author_id(author_id)

    # fill author including their publications
    scholar_publications = scholarly.fill(author,sections=['publications'])
    for publication in self.candinate['publication']:
        for scholar_publication in self.scholar_publications:
            if similarity(publication['title'], scholar_publication['title']) > 0.8:

                publication = {
                    "url": '',
                    "title": '',
                    "year": '',
                    "abstract": '',
                    "citation": '',
                    "topics": '',
                    "type": ''
                }

                print(scholar_publication)
                break

    for scholar_publication in self.scholar_publications:
        print("URL:", scholar_publication['url'])
        print("Title:", scholar_publication['title'])
        print("Year:", scholar_publication['year'])
        print("Abstract:", scholar_publication['abstract'])
        print("Citation:", scholar_publication['citation'])
        print("Topics:", scholar_publication['topics'])
        print("Type:", scholar_publication['type'])
        print("-----")
    for pub in self.candinate['publication']:
        print("Title:", pub['title'])
        print("ResearchGate URL:", pub['researchgate_url'])
        print("Google Scholar URL:", pub['googleScholar_url'])
        print("Semantic URL:", pub['sematic_url'])
        print("-----")
