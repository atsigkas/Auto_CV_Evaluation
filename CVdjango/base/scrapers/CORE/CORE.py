from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def search_and_extract_info(que):
    PATH = r"/CVdjango/base/scrapers/Resources/chromedriver.exe"

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://portal.core.edu.au/conf-ranks/?search=&by=all&source=all&sort=atitle&page=1")

    input_field  = driver.find_element(By.XPATH,'//input[@name="search"]')
    input_field.send_keys(que)

    selection_year = driver.find_element("name","source")
    select = Select(selection_year)
    select.select_by_visible_text('CORE2023')

    button_search  = driver.find_element(By.XPATH,'//input[@value="Search"]')
    button_search.click()

    table = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, '//table'))
    )
    # Get all rows starting from the second one
    rows = table.find_elements(By.XPATH,'.//tr[position() > 1]')

    # Extract the first td from each row and print it
    for row in rows:
        title_td = row.find_element(By.XPATH,'.//td[1]')
        rank_td = row.find_element(By.XPATH, './/td[4]')
    driver.quit()

query = ['ACM International Conference on Research and Development in Information Retrieval',
         'ACM SIGMOD-SIGACT-SIGART Conference on Principles of Database Systems']
for que in query:
    search_and_extract_info(que)


keys = [
    "CORE2023",
    "CORE2021",
    "CORE2020",
    "CORE2018",
    "CORE2017",
    "CORE2014",
    "CORE2013",
    "ERA2010",
    "CORE2008"
]

values = [
    [2023],
    [2021, 2022],
    [2020],
    [2018, 2019],
    [2017],
    [2014, 2015, 2016],
    [2013],
    [2010, 2011, 2012],
    [2008, 2009]
]
year_mapping = dict(zip(keys, values))
#similaroti title
#parameter year ,title

