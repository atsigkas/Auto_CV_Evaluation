import requests
from bs4 import BeautifulSoup
from CVdjango.base.scrapers.utils import *


class ResearchGateScraper:
    def __init__(self, candidate):
        self.candidate = candidate
        self.researchgate_publications = []

    def find_all_papers(self, url, i):
        try:
            print('Page:'+str(i))
            response = requests.get(get_proxy_url(url + '/' + str(i), True))
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', class_='nova-legacy-e-link nova-legacy-e-link--color-inherit nova-legacy-e-link--theme-bare',href=True)
            for link in links:
                href = link.get('href')
                if "researchgate.net/publication" in href:
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
            paginations = soup.find_all('a', class_='nova-legacy-c-button nova-legacy-c-button--align-center nova-legacy-c-button--radius-m nova-legacy-c-button--size-s nova-legacy-c-button--color-grey nova-legacy-c-button--theme-bare',href=True)
            print(paginations)
            for pagination in paginations:
                try:
                    print(pagination)
                    url_split = pagination['href'].split('/')[-1]
                    print(url_split)
                    if str(i+1) in url_split:
                        response = requests.get(get_proxy_url(url + '/' + str(i+1), True))
                        return self.find_all_papers( url, i+1)
                except Exception as error:
                    print(error)
                    print("Error in Pagination")
            return self.researchgate_publications
        except Exception as error:
            print(error)
            print("Problem")

    def check_papers(self):
        for i,publication in enumerate(self.candidate['publication']):
            for researchgate_publication in self.researchgate_publications:
                if similarity(publication['title'],researchgate_publication['title'])>0.8:
                    response = requests.get(get_proxy_url(researchgate_publication['url'],True))
                    # Get the content of the response
                    webpage_html_content = response.text

                    # Create a BeautifulSoup object and specify the parser
                    soup = BeautifulSoup(webpage_html_content, "html.parser")

                    '''
                    researchgate_publication['type'] = soup.select_one(".nova-legacy-e-badge.nova-legacy-e-badge--color-green.nova-legacy-e-badge--display-inline.nova-legacy-e-badge--luminosity-high.nova-legacy-e-badge--size-l.nova-legacy-e-badge--theme-solid.nova-legacy-e-badge--radius-m.research-detail-header-section__badge").text
                    researchgate_publication['year'] = soup.select_one("div.research-detail-header-section__metadata > div:first-child > ul:first-child > li:first-child").text
                    researchgate_publication['abstract'] = soup.select_one("div.nova-legacy-e-text.nova-legacy-e-text--size-m.nova-legacy-e-text--family-sans-serif.nova-legacy-e-text--spacing-none.nova-legacy-e-text--color-grey-800.research-detail-middle-section__abstract").text
                    researchgate_publication['title']  = soup.select_one("h1.nova-legacy-e-text.nova-legacy-e-text--size-xl.nova-legacy-e-text--family-display.nova-legacy-e-text--spacing-none.nova-legacy-e-text--color-grey-900.research-detail-header-section__title").text
                    researchgate_publication['citation'] = soup.select_one("button:first-of-type > div:first-of-type > div:first-of-type > h2:first-of-type").text
                    
                    try:
                        researchgate_publication['type'] = soup.select_one(
                            ".nova-legacy-e-badge.nova-legacy-e-badge--color-green.nova-legacy-e-badge--display-inline.nova-legacy-e-badge--luminosity-high.nova-legacy-e-badge--size-l.nova-legacy-e-badge--theme-solid.nova-legacy-e-badge--radius-m.research-detail-header-section__badge").text
                    except AttributeError:
                        researchgate_publication['type'] = ''  # or some other default value

                    try:
                        researchgate_publication['year'] = soup.select_one(
                            "div.research-detail-header-section__metadata > div:first-child > ul:first-child > li:first-child").text
                    except AttributeError:
                        researchgate_publication['year'] = ''  # or some other default value

                    try:
                        researchgate_publication['abstract'] = soup.select_one(
                            "div.nova-legacy-e-text.nova-legacy-e-text--size-m.nova-legacy-e-text--family-sans-serif.nova-legacy-e-text--spacing-none.nova-legacy-e-text--color-grey-800.research-detail-middle-section__abstract").text
                    except AttributeError:
                        researchgate_publication['abstract'] = ''  # or some other default value

                    try:
                        researchgate_publication['title'] = soup.select_one(
                            "h1.nova-legacy-e-text.nova-legacy-e-text--size-xl.nova-legacy-e-text--family-display.nova-legacy-e-text--spacing-none.nova-legacy-e-text--color-grey-900.research-detail-header-section__title").text
                    except AttributeError:
                        researchgate_publication['title'] = ''  # or some other default value

                    try:
                        researchgate_publication['citation'] = soup.select_one(
                            "button:first-of-type > div:first-of-type > div:first-of-type > h2:first-of-type").text
                    except AttributeError:
                        researchgate_publication['citation'] = ''  # or some other default value
                    '''
                    selectors = {
                        'type': ".nova-legacy-e-badge.nova-legacy-e-badge--color-green.nova-legacy-e-badge--display-inline.nova-legacy-e-badge--luminosity-high.nova-legacy-e-badge--size-l.nova-legacy-e-badge--theme-solid.nova-legacy-e-badge--radius-m.research-detail-header-section__badge",
                        'year': "div.research-detail-header-section__metadata > div:first-child > ul:first-child > li:first-child",
                        'abstract': "div.nova-legacy-e-text.nova-legacy-e-text--size-m.nova-legacy-e-text--family-sans-serif.nova-legacy-e-text--spacing-none.nova-legacy-e-text--color-grey-800.research-detail-middle-section__abstract",
                        'title': "h1.nova-legacy-e-text.nova-legacy-e-text--size-xl.nova-legacy-e-text--family-display.nova-legacy-e-text--spacing-none.nova-legacy-e-text--color-grey-900.research-detail-header-section__title",
                        'citation': "button:first-of-type > div:first-of-type > div:first-of-type > h2:first-of-type"
                    }

                    for key, selector in selectors.items():
                        researchgate_publication[key] = extract_text(soup, selector)

                    self.candidate['publication'][i]['researchgate_url']=researchgate_publication['url']

                    print(researchgate_publication)
                    break


        for researchgate_publication in self.researchgate_publications:
            print("URL:", researchgate_publication['url'])
            print("Title:", researchgate_publication['title'])
            print("Year:", researchgate_publication['year'])
            print("Abstract:", researchgate_publication['abstract'])
            print("Citation:", researchgate_publication['citation'])
            print("Topics:", researchgate_publication['topics'])
            print("Type:", researchgate_publication['type'])
            print("-----")
        for pub in self.candidate['publication']:
            print("Title:", pub['title'])
            print("ResearchGate URL:", pub['researchgate_url'])
            print("Google Scholar URL:", pub['googlescholar_url'])
            print("Semantic URL:", pub['sematic_url'])
            print("-----")

    def update_publication(self, col):
        try:
            for i, pub in enumerate(self.candidate["publication"]):
                new_url = pub['researchgate_url']
                print(new_url)
                # Update only the 'publication' list
                col.update_one(
                    # query
                    {"_id": self.candidate['_id'], "publication.title": pub['title']},
                    # Update: researchgate_url
                    {"$set": {"publication.$.researchgate_url": new_url}}
                )
        except Exception as error:
            print(error)
            print("Couldn't Update")

    def update_researchgate_publication(self, col):
        col.update_one(
            {'_id': self.candidate['_id']},
            {'$push': {"researchgate": {"$each": self.researchgate_publications}}}
        )