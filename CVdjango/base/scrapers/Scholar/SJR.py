from bs4 import BeautifulSoup
import requests

def extract_text(soup, selector):
    element = soup.select_one(selector)
    if element is not None:
        result = element.text
    else:
        return 'FALSE'

    return result

post_body = {
  "cmd": "request.get",
  "url":"https://www.scimagojr.com/journalsearch.php?q=28773&tip=sid&clean=0",
  "maxTimeout": 60000
}

response = requests.post('http://localhost:8191/v1', headers={'Content-Type': 'application/json'}, json=post_body)
response_json=response.json()

webpage_html_content = response_json["solution"]["response"]

soup = BeautifulSoup(webpage_html_content, "html.parser")
tables = soup.find_all('table')
sjr_table = None
for table in tables:
    if "SJR" in table.get_text():
        sjr_table = table
        break
contents = []
for td in table.find_all('td'):
    contents.append(td.get_text())
    print(td.get_text())
sjr_dict_from_table = {contents[i]: float(contents[i+1]) for i in range(0, len(contents), 2)}
print(sjr_dict_from_table)

##if journal

