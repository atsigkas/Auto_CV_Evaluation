from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from ..utils import *
import pandas as pd
import time
import os
import glob

PATH = r"/CVdjango/base/scrapers/Resources/chromedriver.exe"
DIRECTORY = r"C:\Users\stav_\Desktop\projects\Auto_CV_Evaluation\CVdjango\base\scrapers\Resources"
OPTIONS = [
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

def search_and_extract_info(date):

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Set up Chrome to auto-download files to a specified directory
    prefs = {
        "download.default_directory": DIRECTORY,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://portal.core.edu.au/conf-ranks/?search=&by=all&source=all&sort=atitle&page=1")

    try:
        selection_year = driver.find_element("name", "source")
        select = Select(selection_year)
        select.select_by_visible_text(date)

        wait = WebDriverWait(driver, 2)
        button_search = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Search"]')))
        button_search.click()

        button_export = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Export"]')))
        button_export.click()
        time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def rename_file(date):
    directory = r"C:\Users\stav_\Desktop\projects\Auto_CV_Evaluation\CVdjango\base\scrapers\Resources"
    old_path = os.path.join(directory, "CORE.csv")
    new_path = os.path.join(directory, f"{date}.csv")

    try:
        os.rename(old_path, new_path)
        print(f"File renamed from CORE.csv to {date}.csv")
    except Exception as e:
        print(f"An error occurred while renaming the file: {e}")

def core_crawling():
    #delete_csv_files()
    csv_files= check_if_csv_files()
    if not csv_files:
        for date in OPTIONS:
            search_and_extract_info(date)
            rename_file(date)

#create a manp with the ranking

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
    ["2023"],
    ["2021", "2022"],
    ["2020"],
    ["2018", "2019"],
    ["2017"],
    ["2014", "2015", "2016"],
    ["2013"],
    ["2010", "2011", "2012"],
    ["2008", "2009"]
]
year_mapping = dict(zip(keys, values))

ranking = {
    'A*': 1,
    'A': 0.75,
    'B': 0.5,
    'C': 0.25,
}

def check_if_csv_files():
    all_exist = all(os.path.exists(os.path.join(DIRECTORY, f"{option}.csv")) for option in OPTIONS)
    if all_exist:
        print("All required CSV files exist.")
        return True
    else:
        print("Some CSV files are missing.")
        return False
    return False

def delete_csv_files():
    # Construct the path pattern to match CSV files in the specified directory
    path_pattern = os.path.join(DIRECTORY, '*.csv')

    # Use glob to find all CSV files in the directory
    csv_files = glob.glob(path_pattern)

    # Iterate through each CSV file and remove it
    for csv_file in csv_files:
        try:
            os.remove(csv_file)
            print(f'Successfully deleted {csv_file}')
        except Exception as e:
            print(f'Could not delete {csv_file}: {e}')


def check_csv_files(name,year):
    print("### CORE ###")
    found=False
    for key, values in year_mapping.items():
        if year in values:
            csv_file = f"{key}.csv"
            print(f"CSV file found: {csv_file}")
            found = True
            break
    if not found:
        print(f"For the {year} didn't find file")
        return 0


    file_path = os.path.join(DIRECTORY, csv_file)
    df = pd.read_csv(file_path)
    new_column_labels = list('ABCDEFGHI')
    df.columns = new_column_labels

    for index, row in df.iterrows():
        title = row['B'] + ' ' + str(row['C'])
        similarity_text = similarity(name.lower(), title.lower())
        if similarity_text > 0.5:
            print(f"Ours: {name.lower()}")
            print(f"CSV:{title.lower()}")
            print(f"Found the Conference :{title}")
            if row['E'] in ranking.keys():
                print(f"Found:{ranking[row['E']]}")
                return ranking[row['E']]
            else:
                print(f"Not properly ranking")
                return 0
    print(f"Not found : {name.lower()}")
    return 0


