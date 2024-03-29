'''
Pairnw to profile apo api
kai meta varaw gia ka8e publication api
'''
from urllib.parse import urlparse, parse_qs
from scholarly import scholarly
from ..utils import *
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

        scholar_publications = scholarly.fill(author)
        for scholar_publication in author['publications']:
            pub = {
                "url": scholar_publication['author_pub_id'],
                "title": scholar_publication['bib']['title'],
                "year": '',
                "abstract": '',
                "topics": '',
                "type": ''
            }
            self.scholar_publications.append(pub)

        for i, publication in enumerate(self.candidate['publications']):
            found=False
            for scholar_publication in self.scholar_publications:
                if similarity(publication['title'], scholar_publication['title']) > 0.7:
                    found = True
                    scholar_temp = {
                        "container_type": "Publication",
                        "source": "AUTHOR_PUBLICATION_ENTRY",
                        "author_pub_id": scholar_publication['url'],
                        "bib": {
                            "title": scholar_publication['title'],
                            "abstract": scholar_publication['abstract']
                        }
                    }
                    scholarly.fill(scholar_temp)

                    scholar_publication["title"] = scholar_temp["bib"]["title"] if "title" in scholar_temp["bib"] else "Unknown"
                    scholar_publication["year"] = int(scholar_temp["bib"]["pub_year"]) if "pub_year" in scholar_temp["bib"] else 0
                    scholar_publication["abstract"] = scholar_temp["bib"]["abstract"] if "abstract" in scholar_temp["bib"] else "Unknown"
                    scholar_publication["citation"] = scholar_temp["num_citations"] if "num_citations" in scholar_temp else "Unknow"
                    if "conference" in scholar_temp["bib"]:
                        scholar_publication["name_of_type"] = scholar_temp["bib"]["conference"]
                        scholar_publication["type"] = "conference"
                    elif "journal" in scholar_temp["bib"]:
                        scholar_publication["name_of_type"] = scholar_temp["bib"]["journal"]
                        scholar_publication["type"] = "journal"
                    else:
                        scholar_publication["type"] = "Unknown"
                        scholar_publication["name_of_type"] = "Unknown"

                    self.candidate['publications'][i]['googlescholar_url'] = scholar_publication['url']
                    self.candidate['publications'][i]['abstract'] = scholar_publication['abstract']
                    self.candidate['publications'][i]['type'] = scholar_publication['type']
                    self.candidate['publications'][i]['name_of_type'] = scholar_publication['name_of_type']

                    break

            if not found:
                self.scholar_publications.remove(scholar_publication)
        self.candidate['googlescholar'] = self.scholar_publications

    def update_publication(self, col):
        try:
            for i, pub in enumerate(self.candidate["publications"]):
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