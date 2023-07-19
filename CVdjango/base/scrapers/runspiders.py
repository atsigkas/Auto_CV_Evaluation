import requests
from bs4 import BeautifulSoup
from CVdjango.base.scrapers.utils import *
from CVdjango.base.db.utils import *


def search(response, researchgate):
    soup = BeautifulSoup(response.text, 'html.parser')
    found = False
    for link in soup.find_all('a', href=True):
        if "profile" in link['href'] or "scientific-contributions" in link['href']:
            #url_split= link['href'].split('/', 1)[1]
            print(similarity(researchgate['author'], link.text),link.text)
            if similarity(researchgate['author'], link.text) > 0.7 and found is False:
                found = True
                researchgate['researchgate_url'] = link['href']
                print(found,researchgate)
                return researchgate


def get_and_apply(url, callback, researchgate):
    response = requests.get(get_proxy_url(url, True))
    if response.status_code == 200:
        return callback(response, researchgate)


def search_author(author,paper,website):

    author_url = author.replace(" ", "+")
    paper_url = paper.replace(" ", "+")
    url = "https://www.google.com/search?q="+website+'+'+author_url+'+'+paper_url

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
        'author': '',
        "email": '',
        "phone": '',
        "researchgate_url": '',
        "googleScholar_url": '',
        "sematic_url": '',
    }
    researchgate['author']=author

    for url, score in similarity_table:
        if score > 0.8:
            try:
                get_and_apply(url,search,researchgate)
                print(researchgate)
                return researchgate
            except Exception as error:
                print(error)
                print("Problem Found Author")
    return None



def update_candinate(col,candinate,id):
    result = col.update_one(
        {"_id": id},
        # Update: researchgate_url
        {"$set": {"researchgate_url": candinate['researchgate_url']}}
    )