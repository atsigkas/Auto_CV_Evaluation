from bs4 import BeautifulSoup
from ..utils import *


def search_type(name,date):
    print("### SJR ###")
    name_with_plus = name.replace(" ", "+")
    url = "https://www.google.com/search?q="+"site:scimagojr.com"+"+"+name_with_plus
    response = get_proxy_url(url, True)

    soup = BeautifulSoup(response, "html.parser")
    links = soup.find_all('a', href=True)
    urls = []
    for link in links:
        url = link['href']
        if "https://www.scimagojr.com/" in url:
            urls.append(url)

    for url in urls[:3]:
        try:
            ranking = find_value_by_date(url,name, date)
            if ranking != 0:
                return ranking
        except Exception as error:
            print(f"Problem Found {name}")
            print(error)
    return 0

def find_value_by_date(url,name,date):

    response = get_proxy_url(url,True)

    soup = BeautifulSoup(response, "html.parser")
    title=extract_text(soup, "h1:first-of-type").strip()
    similarity_score = similarity(title , name)

    if similarity_score > 0.3:
        tables = soup.find_all('table')
        sjr_table = None
        for table in tables:
            if "SJR" in table.get_text():
                sjr_table = table
                break
        if sjr_table is not None:
            for row in sjr_table.find_all('tr'):
                if row:
                    cols = row.find_all('td')
                    if cols:
                        if len(cols) > 0 and date in cols[0].get_text():
                            print(f"The name  of the type from the publication: {name}")
                            print(f"The name  of the type from the website: {title}")
                            print(f"Similarity score : {similarity_score}")
                            sjr_value = float(cols[1].get_text())
                            if sjr_value > 0.47:
                                value = 1
                            elif sjr_value > 0.26:
                                value = 0.75
                            elif sjr_value > 0.14:
                                value = 0.5
                            else:
                                value =0.25
                            return value # Assuming the value is in the next
        return 0
    return 0

