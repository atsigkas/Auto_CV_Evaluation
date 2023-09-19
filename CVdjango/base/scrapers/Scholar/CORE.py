from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH=r"C:\Users\stav_\Desktop\projects\Auto_CV_Evaluation\CVdjango\base\scrapers\Resources\chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://portal.core.edu.au/conf-ranks/?search=&by=all&source=all&sort=atitle&page=1")

input_field  = driver.find_element(By.XPATH,'//input[@name="search"]')
input_field.send_keys('Information Retrieval Facility Conference')
button_search  = driver.find_element(By.XPATH,'//input[@value="Search"]')
button_search.click()

table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//table'))
)
# Get all rows starting from the second one
rows = table.find_elements(By.XPATH,'.//tr[position() > 1]')

# Extract the first td from each row and print it
for row in rows:
    first_td = row.find_element(By.XPATH,'.//td[1]')
    link=row
    print(first_td.text)
link.click()

year_rank  = driver.find_element(By.XPATH,"//div[text()='Source: CORE2018']")
rank = driver.find_element(By.XPATH,"//div/following-sibling::div[contains(text(), 'Rank')]")
print(rank.text)

driver.quit()