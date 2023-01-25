import selenium
from bs4 import BeautifulSoup as bs
import requests
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from scrape.basketball.helpers import col_names


BASE_URL = "https://www.easycredit-bbl.de/"
s = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
start_season = 2005
end_season = 2021


def selenium_driver(url):
    driver_location = "../../chromedriver"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    d = webdriver.Chrome(driver_location)
    d.get(url)
    time.sleep(1)
    return d


def get_games_hrefs(d):
    games_hrefs = []
    bs_main = bs(d.page_source, "html.parser")
    seasons = [f"Saison {s_} / {s_ + 1}" for s_ in range(start_season, end_season + 1)]
    for i, season in enumerate(seasons):
        season_str = season.replace("Saison", "").replace(" ", "")
        print(season_str)
        d.find_element_by_xpath("(//div[@class=' css-1wy0on6'])[1]").click()
        time.sleep(0.2)
        d.find_element_by_xpath(f"//div[contains(text(),'{season}')]").click()
        time.sleep(0.2)

        for spieltag in range(1, 35):
            d.find_element_by_xpath("//div[@data-testid='matchday-selector-delayed']//div[@class=' css-1wy0on6']").click()
            time.sleep(0.2)
            d.find_element_by_xpath(f"//div[contains(text(),'{spieltag}. Spieltag')]").click()
            time.sleep(0.2)
            d.find_element_by_xpath("//button[@data-testid='applyFilterButton']").click()
            time.sleep(1)

            if spieltag == 1 and i == 0:
                d.find_element_by_xpath("//button[@data-testid='games-toggle']").click()
                time.sleep(0.2)

            f = bs(d.page_source, "html.parser")
            hrefs = [a.get("href") for a in f.find_all("a", {"rel": "noreferrer"})][0::4]
            print(len(hrefs), hrefs)

    # df_href = pd.DataFrame(games_hrefs, columns=['season', 'part', 'href'])
    # df_href.to_csv("../../data/vtb/hrefs.csv")
    return games_hrefs


driver = selenium_driver(f"{BASE_URL}saison/spielplaene_liga-pokalspiele/hauptrunde")
get_games_hrefs(driver)

hrefs = pd.read_csv("../../data/vtb/hrefs.csv")
games_data = []
for i, (index, season, season_part, game_h) in hrefs.iterrows():
    print(game_h)
    driver.get(game_h)
    time.sleep(1)
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(0.1)

    rnd = None
    bs_game_card = bs(driver.page_source, "html.parser")
    q_scores = bs_game_card.find("div", {"class": "mbt-v2-game-quarter-scores"})
    if not q_scores:
        game_row = [season, season_part, rnd,
                    date_string, ] ### end here I guess?
        games_data.append(game_row)
    quarters = [q.text.strip().split(" : ") for q in q_scores.find_all("span")]
    h_quarters = [q_pair[0] for q_pair in quarters] + (8 - len(quarters)) * [None]
    a_quarters = [q_pair[1] for q_pair in quarters] + (8 - len(quarters)) * [None]
    h_code = bs_game_card.find("div", {"class": "mbt-v2-game-team-logo-a"}).find("a").get("team_id")
    a_code = bs_game_card.find("div", {"class": "mbt-v2-game-team-logo-b"}).find("a").get("team_id")

    driver.find_element_by_xpath(f"//div[@id='15-400-tab-1']").click()
    time.sleep(1.2)

    bs_box_score = bs(driver.page_source, "html.parser")
    teams_div = bs_box_score.find("div", {"class": "mbt-v2-header"})
    teams_div_list = teams_div.text.strip().split("\n")
    h_name = teams_div_list[0].strip()
    a_name = teams_div_list[4].strip()
    h_score = int(teams_div_list[1].strip())
    a_score = int(teams_div_list[3].strip())

    match_info = [s.text.strip() for s in bs_box_score.find("div", {"class": "mbt-v2-game-main-information"}).find_all("span")]
    date_split = match_info[0].split("/")
    date_string = f"{date_split[1]}/{date_split[0]}/{date_split[2]}"
    game_time = match_info[1]
    venue = match_info[2]
    attendance = None
    if match_info[3].isnumeric():
        attendance = int(match_info[3])

    ref_text = bs_box_score.find(text=re.compile('Referees'))
    ref1, ref2, ref3 = None, None, None
    if ref_text:
        refs = ref_text.parent.parent.text.strip().split("Referees:")[1]
        ref1, ref2, ref3 = [ref.strip() for ref in refs.split(",")]

    sums_h_td, sums_a_td = [g_.parent.parent for g_ in bs_box_score
                            .find("table", {"id": "mbt-v2-game-boxscore-table"})
                            .find_all(text=re.compile('Sums'))]
    sums_h = [s.text.strip() for s in sums_h_td.find_all("td")]
    sums_a = [s.text.strip() for s in sums_a_td.find_all("td")]
    h_stats = sums_h[2].split("/") + sums_h[4].split("/") + sums_h[8].split("/") + sums_h[10:13] + \
        [sums_h[13], sums_h[17], sums_h[16], sums_h[18], sums_h[19], sums_h[14], sums_h[15], sums_h[20]]
    a_stats = sums_a[2].split("/") + sums_a[4].split("/") + sums_a[8].split("/") + sums_a[10:13] + \
        [sums_a[13], sums_a[17], sums_a[16], sums_a[18], sums_a[19], sums_a[14], sums_a[15], sums_a[20]]

    game_row = [
        season, season_part, rnd,
        date_string, game_time, venue,
        attendance, ref1, ref2, ref3,
        h_name, a_name, h_code, a_code,
        h_score, a_score, *h_quarters,
        *a_quarters, *h_stats, *a_stats
    ]

    print(game_row)
    games_data.append(game_row)
df_vtb = pd.DataFrame(data=games_data, columns=col_names)
df_vtb.to_csv("../../data/vtb/vtb_games.csv", index=False)

driver.close()


