import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from urllib.parse import urlencode
from difflib import SequenceMatcher

import re

API_KEY = '7335ee33-d1e8-4a2a-9166-672f20fcaece'
def get_proxy_url(url,UsingProxy):
    if UsingProxy is True:
        payload = {'api_key': API_KEY, 'url': url}
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
        return proxy_url
    else:
        return url

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def search(response, researchgate):
    soup = BeautifulSoup(response.text, 'html.parser')
    found = False
    for link in soup.find_all('a', href=True):
        if "profile" in link['href'] or "scientific-contributions" in link['href']:
            url_split= link['href'].split('/', 1)[1]
            if similarity(researchgate['author'], url_split) > 0.7 and found is False:
                found = True
                researchgate['url'] = 'https://www.researchgate.net/'+link['href']
                return researchgate

def get_and_apply(url, callback, researchgate):
    response = requests.get(get_proxy_url(url, True))
    if response.status_code == 200:
        return callback(response, researchgate)


website='site:researchgate.net'
original_name_author='Grigorios Tsoumakas'
author='Grigorios Tsoumakas'
author2 = author.replace(" ", "+")
paper='Dense Distributions from Sparse Samples: Improved Gibbs Sampling Parameter Estimators for LDA'
paper2=paper.replace(" ", "+")
url = "https://www.google.com/search?q="+website+'+'+author2+'+'+paper2
#url='https://www.researchgate.net/profile/Grigorios-Tsoumakas'

try:
    response = requests.get(get_proxy_url(url,True))
    # Get the content of the response
    webpage_html_content = response.text

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(webpage_html_content, "html.parser")

    # After creating the soup, we can extract all href attributes
    links = soup.find_all('a', href=True)

    similarity_scores = []
    urls = []

    # Check each link
    for link in links:
        url = link['href']
        if "researchgate.net/publication" in url:
            url_split = url.split('_', 1)[1]
            similarity_scores.append(similarity(url_split, paper))
            urls.append(url)

    similarity_table = list(zip(urls, similarity_scores))
    similarity_table.sort(key=lambda x: x[1], reverse=True)
    print(similarity_table)

    researchgate ={
        "author":'Grigorios Tsoumakas',
        "id":'',
        "url":'',
        "papers":[{
            "title",
            "year",
            "abstract",
            "citation",
            "topics",
            "type"
        }]
    }

    for url, score in similarity_table:
        if score > 0.8:
            try:
                get_and_apply(url,search,researchgate)
                print(researchgate)
            except Exception as error:
                print(error)
                print("Problem Found Author")


except Exception as error:
    print(error)
    print("Problem")

try:
    for url in researchgate['']:


except Exception as error:
    print(error)
    print("Problem")
