import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import time
from selenium_init import selenium_driver
import re
import sys
import json
import glob
import os


def get_venues_data(driver, venues, exceptions):
    capacities = []
    for index, venue in enumerate(venues):
        if venue in exceptions:
            capacities.append(exceptions[venue])
            continue
        if venue is np.nan:
            continue
        search_value = venue
        if venue_types[sport] not in venue:
            search_value = f"{venue} {venue_types[sport]} wikipedia"
        capacity = 0
        driver.get(f"{BASE_URL}/search?&q={search_value}")
        time.sleep(1)
        google_search = bs(driver.page_source, "html.parser")
        hrefs = [a.get("href") for a in google_search.find_all("a")]
        wiki = next(href for href in hrefs if href and "en.wikipedia" in href)
        driver.get(wiki)
        time.sleep(1)
        wiki_page = bs(driver.page_source, "html.parser")
        capacity_info = wiki_page.find("th", string="Capacity").nextSibling
        capacity_info_lines = capacity_info.get_text(strip=True, separator='\n').splitlines()
        sport_info = next((info for info in capacity_info_lines if sport in info or sport.capitalize() in info), None)
        if sport_info is not None:
            re_res = re.findall('[0-9]+', sport_info.replace(",", ""))
            if len(re_res) > 0:
                capacity = re_res[0]
        if capacity == 0:
            capacity = int(re.findall('[0-9]+', capacity_info.text.replace(",", ""))[0])
        capacities.append(capacity)
        print(index, venue, capacity)
    venues_df = pd.DataFrame({"venues": venues, "capacity": capacities})
    venues_df.to_csv(f"../../data/{sport}/{league}/{league}_venues.csv", index=False)


if __name__ == "__main__":
    BASE_URL = "https://www.google.com"
    s = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

    venue_types = {"football": "STADIUM", "basketball": "ARENA", "handball": "ARENA"}
    _, sport, league = list(sys.argv)
    if sport == "football":
        files = os.path.join(f"../../data/{sport}/{league}/{league}_games*.csv")
        files = glob.glob(files)
        games = pd.concat(map(pd.read_csv, files), ignore_index=True)
    else:
        games = pd.read_csv(f"../../data/{sport}/{league}/{league}_games.csv")
    venues_list = list(games["Venue"].unique())
    print(venues_list)
    exit(0)
    exceptions_file = open(f"../{sport}/{league}/{league}_venues_exceptions.json")
    exceptions_dict = json.load(exceptions_file)

    CHROME_DRIVER_PATH = "../../scrape/other/chromedriver"
    d = selenium_driver(BASE_URL, CHROME_DRIVER_PATH)
    get_venues_data(d, venues_list, exceptions_dict)
    d.close()

