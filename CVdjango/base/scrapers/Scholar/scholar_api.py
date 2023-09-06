'''
Pairnw to profile apo api
kai meta varaw gia ka8e publication api
'''
from urllib.parse import urlparse, parse_qs
from scholarly import scholarly
from CVdjango.base.scrapers.utils import *
import json
import requests

def extract_scholar_id(url):
    try:
        # Parse the URL
        parsed_url = urlparse(url)

        # Parse the query string
        query_string = parse_qs(parsed_url.query)

        # Get the author ID
        author_id = query_string['user'][0]
    except Exception:
        print(f"Error to extract author id this url: '{url}'")

    return author_id

class ScholarAPI:
    def __init__(self, candidate):
        self.candidate = candidate
        self.scholar_publications = []


    def check_papers(self):
        # search by unique author id
        author_id = extract_scholar_id(self.candidate['googlescholar_url'])
        author = scholarly.search_author_id(author_id)

        # fill author including their publications
        scholar_publications = scholarly.fill(author)
        for scholar_publication in author['publications']:
            pub = {
                "url": scholar_publication['author_pub_id'],
                "title": scholar_publication['bib']['title'],
                "year": '',
                "abstract": '',
                "citation": '',
                "topics": '',
                "type": '',
                "embeddings": ''
            }
            self.scholar_publications.append(pub)

        for i, publication in enumerate(self.candidate['publication']):
            for scholar_publication in self.scholar_publications:
                if similarity(publication['title'], scholar_publication['title']) > 0.8:
                    scholar_temp = {
                        "container_type": "Publication",
                        "source": "AUTHOR_PUBLICATION_ENTRY",
                        "author_pub_id": scholar_publication['url'],
                        "bib": {
                            "title": scholar_publication['title']
                        }
                    }
                    scholarly.fill(scholar_temp)
                    print(json.dumps(scholar_temp, indent=4))
                    scholar_publication["title"] = scholar_temp["bib"]["title"] if "title" in scholar_temp["bib"] else "Unknown"
                    scholar_publication["year"] = int(scholar_temp["bib"]["pub_year"]) if "pub_year" in scholar_temp["bib"] else 0
                    scholar_publication["abstract"] = scholar_temp["bib"]["abstract"] if "abstract" in scholar_temp["bib"] else "Unknown"
                    scholar_publication["citation"] = scholar_temp["num_citations"] if "num_citations" in scholar_temp else "Unknow"

                    self.candidate['publication'][i]['googlescholar_url'] = scholar_publication['url']

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
        for pub in self.candidate['publication']:
            print("Title:", pub['title'])
            print("ResearchGate URL:", pub['researchgate_url'])
            print("Google Scholar URL:", pub['googlescholar_url'])
            print("Semantic URL:", pub['sematic_url'])
            print("-----")
        self.candidate['googlescholar'] = self.scholar_publications

    def update_publication(self, col):
        try:
            for i, pub in enumerate(self.candidate["publication"]):
                new_url = pub['googlescholar_url']
                print(new_url)
                # Update only the 'publication' list
                col.update_one(
                    # query
                    {"_id": self.candidate['_id'], "publication.title": pub['title']},
                    # Update: researchgate_url
                    {"$set": {"publication.$.googlescholar_url": new_url}}
                )
        except Exception as error:
            print(error)
            print("Couldn't Update")

    def update_googlescholar_publication(self, col):
        col.update_one(
            {'_id': self.candidate['_id']},
            {'$push': {"googlescholar": {"$each": self.scholar_publications}}}
        )

    def insert_researchgate_candidate(self, col):
        col.insert_one(self.candidate)