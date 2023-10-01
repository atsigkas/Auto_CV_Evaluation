import requests
from bs4 import BeautifulSoup
from ..utils import *
import json


class ResearchGateScraper:
    def __init__(self, candidate):
        self.candidate = candidate
        self.researchgate_publications = []

    def find_all_papers(self, url, i):
        """
        This function is retrospective and takes the all the publications links
        @param self
        @return: same function
        """
        try:
            print('Page:'+str(i))
            print(f"Profile Author in ResearchGate:{url}")
            response = get_proxy_url(url + '/' + str(i), True)

            soup = BeautifulSoup(response, 'html.parser')
            links = soup.find_all('a', class_='nova-legacy-e-link nova-legacy-e-link--color-inherit nova-legacy-e-link--theme-bare',href=True)
            for link in links:
                href = link.get('href')
                if "researchgate.net/publication" in href:
                    print(href)
                    publication = {
                        "url": href,
                        "title": link.get_text(),
                        "year":'',
                        "abstract":'',
                        "citation":'',
                        "topics":'',
                        "type":''
                    }
                    self.researchgate_publications.append(publication)
                    print(len(self.researchgate_publications))
            paginations = soup.find_all('a',class_='nova-legacy-c-button nova-legacy-c-button--align-center nova-legacy-c-button--radius-m nova-legacy-c-button--size-s nova-legacy-c-button--color-grey nova-legacy-c-button--theme-bare',href=True)
            print(paginations)
            page_numbers = []
            for pagination in paginations:
                span = pagination.find('span', class_='nova-legacy-c-button__label')
                if span is not None:
                    page_numbers.append(span.text)

            print(page_numbers)
            for pagination in page_numbers:
                try:
                    #print('Page:'+pagination)
                    #url_split = pagination['href'].split('/')[-1]
                    #print(url_split)
                    #if str(i+1) in url_split:
                    #response = get_proxy_url(url + '/' + str(i+1), True)
                    return self.find_all_papers( url, i+1)
                except Exception as error:
                    print("Error in Pagination")
                    print(error)
            return self.researchgate_publications
        except Exception as error:
            print("Problem in find_all_papers")
            print(error)


    def check_papers(self):
        """
        We go to a publication page and we are extracting the necessary information
        :return: It doesn't return something
        """
        for i,publication in enumerate(self.candidate['publication']):
            for researchgate_publication in self.researchgate_publications:
                if similarity(publication['title'].lower(),researchgate_publication['title'].lower())>0.8:
                    response = get_proxy_url(researchgate_publication['url'],True)

                    # Create a BeautifulSoup object and specify the parser
                    soup = BeautifulSoup(response, "html.parser")

                    print(researchgate_publication['title'])
                    selectors = {
                        'type': ".nova-legacy-e-badge.nova-legacy-e-badge--color-green.nova-legacy-e-badge--display-inline.nova-legacy-e-badge--luminosity-high.nova-legacy-e-badge--size-l.nova-legacy-e-badge--theme-solid.nova-legacy-e-badge--radius-m.research-detail-header-section__badge",
                        'year': "div.research-detail-header-section__metadata > div:first-child > ul:first-child > li:first-child",
                        'abstract': "div.nova-legacy-e-text.nova-legacy-e-text--size-m.nova-legacy-e-text--family-sans-serif.nova-legacy-e-text--spacing-none.nova-legacy-e-text--color-grey-800.research-detail-middle-section__abstract",
                        'title': "h1.nova-legacy-e-text.nova-legacy-e-text--size-xl.nova-legacy-e-text--family-display.nova-legacy-e-text--spacing-none.nova-legacy-e-text--color-grey-900.research-detail-header-section__title",
                        'citation': "button:first-of-type > div:first-of-type > div:first-of-type > h2:first-of-type",
                        'name_of_type':"div:first-of-type > ul:first-of-type > li:nth-child(2)>a"
                    }

                    candidate_li_elements = soup.find_all(
                        'li',
                        {'class': 'nova-legacy-e-list__item'}
                    )

                    # Check the text of each element to find the ones containing 'Conference:'
                    conference_li = next(
                        (el for el in candidate_li_elements if 'conference:' in el.get_text(strip=True).lower()), None)

                    # If the element is found, extract its text
                    print('###')
                    print(conference_li)

                    if conference_li:
                        conference_text = conference_li.get_text(strip=True)
                        #conference_text = conference_text.replace('Conference: ', '')
                    else:
                        conference_text = "NO"

                    for key, selector in selectors.items():
                        researchgate_publication[key] = extract_text(soup, selector)

                    self.candidate['publication'][i]['researchgate_url'] = researchgate_publication['url']
                    self.candidate['publication'][i]['abstract'] = researchgate_publication['abstract']
                    self.candidate['publication'][i]['type'] = researchgate_publication['type']
                    if conference_text=="NO":
                        self.candidate['publication'][i]['name_of_type'] = researchgate_publication['name_of_type']
                    else:
                        self.candidate['publication'][i]['name_of_type'] = conference_text
                        researchgate_publication['name_of_type']=conference_text
                    # January 2006
                    if researchgate_publication['year'] != "Unknown":
                        researchgate_publication['year'] = researchgate_publication['year'].split()[1]
                        self.candidate['publication'][i]['year'] = researchgate_publication['year']

                    print(json.dumps(researchgate_publication, indent=4))
                    break
        self.candidate['researchgate'] = self.researchgate_publications

    def update_publication(self, col):
        try:
            for i, pub in enumerate(self.candidate["publication"]):
                new_url = pub['researchgate_url']
                abstract = pub['abstract']
                # Update only the 'publication' list
                col.update_one(
                    # query
                    {"_id": self.candidate['_id'], "publication.title": pub['title']},
                    # Update: researchgate_url
                    {"$set": {"publication.$.researchgate_url": new_url}
                    }
                )
        except Exception as error:
            print(error)
            print("Couldn't Update")

    def update_researchgate_publication(self, col):
        col.update_one(
            {'_id': self.candidate['_id']},
            {'$push': {"researchgate": {"$each": self.researchgate_publications}}}
        )
    def insert_researchgate_candidate(self, col):
        col.insert_one(self.candidate)