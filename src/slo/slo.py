# This script goes through KZS seasons and writes basic info
# about games (including the game's hyperref) into a CSV.
import os
# Each line in the output CSV consists of:
# Season, Round, Date, Time, Home team, Away team, Home score, Away score, Href


import pandas as pd
import json
import numpy as np
from bs4 import BeautifulSoup
import time

from src.slo.col_names import col_names_main_info
from src.slo.col_names import col_names_play_by_play
from src.slo.col_names import col_names_box_score
from src.slo.col_names import col_names_score_evolution
from src.slo.col_names import col_names_comparison

from src.slo.get_stats.get_main_info import get_main_info
from src.slo.get_stats.get_box_score import get_box_score
from src.slo.get_stats.get_score_evolution import get_score_evolution
from src.slo.get_stats.get_play_by_play import get_play_by_play
from src.slo.get_stats.get_comparison import get_comparison

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException

from src.other.venues import VenueScraper


def selenium_driver(url, driver_path):
    options = Options()
    options.add_argument("--headless")
    service = Service(executable_path=driver_path)
    wd = webdriver.Firefox(options=options, service=service)
    wd.get(url)
    time.sleep(2)
    return wd


def extract_info(bs_page, season, stage):
    schedule = bs_page.find("table", {"id": "mbt-v2-schedule-table"})
    games = []
    if schedule:
        table = schedule.find("tbody")
        rows = table.find_all("tr")
        for row in rows:
            row_cells = row.find_all("td")
            rnd = row_cells[0].text.strip()
            id_ = row_cells[1].find("a").get("game_id")
            datetime = row_cells[1].text.strip()
            if " " in datetime:
                date, time_ = datetime.split(" ")
            else:
                date = datetime
                time_ = ""
            date = date.replace(".", "/")
            h_team = row_cells[2].text.strip()
            a_team = row_cells[4].text.strip()
            h_score, a_score = row_cells[3].text.strip().split(":")
            href = row_cells[3].find("a").get("href")
            played = False if h_score == "20" and a_score == "0" or h_score == "0" and a_score == "20" else True
            games.append([season, stage, rnd, id_, played, date, time_, h_team, a_team, h_score, a_score, href])
    print(games)
    return games


def get_games(d):
    skip_stages = {"2. del": ["2. del-Liga za prvaka", "2. del-Finale"],
                   "Razigravanje": ["Razigravanje-Polfinale-finale"],
                   "2. del-2. del": ["2. del"],
                   "3. del": ["3. del-Finale"]}
    games = []
    bs_main = BeautifulSoup(d.page_source, "html.parser")
    seasons = [(opt.text.strip(), opt.get("value")) for opt in
               bs_main.find("select", {"id": "33-303-filter-season"}).find_all("option")]

    # Go through all seasons
    for i, (season_text, season_value) in enumerate(seasons):
        season_str = season_text.replace("-", "/")
        print(season_str)
        d.find_element("xpath", f"//select[@id='33-303-filter-season']/option[@value={season_value}]").click()
        time.sleep(2)
        d.find_element("xpath", f"//div[@data-type='results_only']").click()
        time.sleep(2)
        bs_season = BeautifulSoup(d.page_source, "html.parser")
        stages = [(opt.text.strip(), opt.get("value")) for opt in
                  bs_season.find("select", {"id": "33-303-filter-stage"}).find_all("option")]
        stage_texts = [t for t, v in stages]
        for k in range(5):
            # Go through all stages of season
            for j, (stage_text, stage_value) in enumerate(stages[1:]):
                print(stage_text)
                if stage_text in skip_stages and len(set(skip_stages[stage_text]).intersection(set(stage_texts))) > 0:
                    print("Skip")
                    continue
                d.find_element("xpath", f"//select[@id='33-303-filter-stage']/option[@value={stage_value}]").click()
                time.sleep(2)
                bs_stage = BeautifulSoup(d.page_source, "html.parser")
                hrefs = extract_info(bs_stage, season_str, stage_text)
                pages = bs_stage.find("div", {"id": "schedule"}).find("ul", {"class": "mbt-v2-pagination"})

                # If there are more than one page, go through all pages
                if pages:
                    pages = pages.find_all("li")
                    for page in pages[1:-1]:
                        id_ = page.find("a").get("id")
                        d.find_element("xpath", f"//a[@id='{id_}']").click()
                        time.sleep(2)
                        bs_stage = BeautifulSoup(d.page_source, "html.parser")
                        hrefs.extend(extract_info(bs_stage, season_str, stage_text))
                if len(hrefs) > 0:
                    games.extend(hrefs)
    games_df = pd.DataFrame(data=np.unique(np.array(games), axis=0), columns=["Season", "Stage", "Round", "ID",
                                                                              "Played", "Date", "Time",
                                                                              "H_Team", "A_Team", "H_Score",
                                                                              "A_Score", "Href"])
    games_df.to_parquet(f"{DATA_DIR}/games/parquet/games.parquet", index=False)


def get_games_data(d):
    games = pd.read_parquet(f"{DATA_DIR}/games/parquet/games.parquet")
    games['json'] = games.apply(lambda x: x.to_json(), axis=1)
    start = 0
    for i, game_data_str in enumerate(games["json"].iloc[start:]):
        game_data = json.loads(game_data_str)
        game_dir_path = f"{DATA_DIR}/games/parquet/{game_data['ID']}"
        if not os.path.exists(game_dir_path):
            os.mkdir(game_dir_path)
        if game_data["Played"]:
            print(i + start, game_data["Href"])
            if len([name for name in os.listdir(game_dir_path)
                    if os.path.isfile(os.path.join(game_dir_path, name))]) == 5:
                continue

            d.get(game_data["Href"])
            time.sleep(2)
            for stat, function, columns, data_name in STATS:
                file_path = f"{DATA_DIR}/games/parquet/games/{game_data['ID']}/{stat}.parquet"
                if not os.path.exists(file_path):
                    try:
                        d.find_element("xpath", f"//div[@data-name='{data_name}']").click()
                        time.sleep(2)
                    except NoSuchElementException:
                        print(f"Tab {data_name} not found!")
                        continue
                    bs_game = BeautifulSoup(d.page_source, "html.parser")
                    stat_data = function(bs_game, game_data, BASE_URL)
                    if len(stat_data) == 0:
                        print(f"No {stat}")
                    else:
                        col_names = [c for c, t in columns]
                        df = pd.DataFrame(data=stat_data, columns=col_names)
                        for col_name, col_type in columns:
                            df[col_name] = df[col_name].astype(col_type)
                        df.to_parquet(file_path, index=False)


def init_games_data():
    games_data = {}
    for description, _, _, _ in STATS:
        games_data[description] = []
    return games_data


def join_seasons_data():
    dir_path = f"{DATA_DIR}/games/parquet"
    games_data = init_games_data()
    games = pd.read_parquet(f"{dir_path}/games.parquet")
    for game_id in games["ID"]:
        for description, _, _, _ in STATS:
            stat_path = f"{dir_path}/games/{game_id}/{description}.parquet"
            if os.path.exists(stat_path):
                games_data[description].append(pd.read_parquet(stat_path))

    for description, _, _, _ in STATS:
        pd.concat(games_data[description]).to_parquet(f"{dir_path}/{description}.parquet")


def get_venues():
    venue_scraper = VenueScraper(DATA_DIR, DRIVER_PATH, "basketball", "arena")
    # venue_scraper.get_capacity_data()
    # venue_scraper.get_location_data()
    venue_scraper.merge_files()


if __name__ == "__main__":
    BASE_URL = "https://www.kzs.si/"
    DATA_DIR = "../../data/slo"
    DRIVER_PATH = "../other/geckodriver"

    STATS = [
        ("box_score", get_box_score, col_names_box_score, "boxscore"),
        ("main_info", get_main_info, col_names_main_info, "home"),
        ("score_evolution", get_score_evolution, col_names_score_evolution, "game_development"),
        ("play_by_play", get_play_by_play, col_names_play_by_play, "play_by_play"),
        ("comparison", get_comparison, col_names_comparison, "advanced_stats")
        ]

    # driver = selenium_driver(f"{BASE_URL}clanek/Tekmovanja/Liga-Nova-KBM/cid/66", DRIVER_PATH)
    # get_games(driver)
    # get_games_data(driver)
    get_venues()
    join_seasons_data()
