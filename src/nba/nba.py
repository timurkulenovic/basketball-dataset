from nba_api.stats.endpoints import leaguegamefinder
import os


import pandas as pd
import json
import time

from src.nba.col_names import col_names_main_info
from src.nba.col_names import col_names_play_by_play
from src.nba.col_names import col_names_box_score
from src.nba.col_names import col_names_score_evolution
from src.nba.col_names import col_names_comparison

from src.nba.get_stats.get_main_info import get_main_info
from src.nba.get_stats.get_box_score import get_box_score

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException

from src.other.venues import VenueScraper


pd.set_option('display.expand_frame_repr', False)


def selenium_driver(url, driver_path):
    options = Options()
    options.add_argument("--headless")
    service = Service(executable_path=driver_path)
    wd = webdriver.Firefox(options=options, service=service)
    wd.get(url)
    time.sleep(2)
    return wd


def get_games():
    games_data = []
    seasons = [f"{year}-{str(year + 1)[-2:]}" for year in range(2000, 2023)]
    stages = ["Regular Season", "Playoffs"]

    for season in seasons:
        print(season)
        for stage in stages:
            time.sleep(2)
            games = leaguegamefinder.LeagueGameFinder(league_id_nullable="00",
                                                      season_nullable=season,
                                                      season_type_nullable=stage).get_data_frames()[0]
            for game_id in games["GAME_ID"].unique():
                games_with_id = games[games.GAME_ID == game_id]
                matchup = games_with_id[games_with_id['MATCHUP'].str.contains("vs.")].iloc[0]["MATCHUP"]
                h_team_id, a_team_id = matchup.split(" vs. ")

                h_team_data = games_with_id[games_with_id["TEAM_ABBREVIATION"] == h_team_id].iloc[0]
                a_team_data = games_with_id[games_with_id["TEAM_ABBREVIATION"] == a_team_id].iloc[0]

                h_team, a_team = h_team_data["TEAM_NAME"], a_team_data["TEAM_NAME"]
                h_score, a_score = h_team_data["PTS"], a_team_data["PTS"]
                date = games_with_id.iloc[0]["GAME_DATE"]

                games_data.append([season, stage, game_id, date, h_team, a_team,
                                   h_team_id, a_team_id, h_score, a_score])

    games_df = pd.DataFrame(data=games_data, columns=["Season", "Stage", "ID", "Date",
                                                      "H_Team", "A_Team", "H_Team_ID",
                                                      "A_Team_ID", "H_Score", "A_Score"])
    games_df.to_parquet(f"{DATA_DIR}/games/parquet/games.parquet", index=False)


def get_games_data():
    games = pd.read_parquet(f"{DATA_DIR}/games/parquet/games.parquet")
    games['json'] = games.apply(lambda x: x.to_json(), axis=1)
    start = 0
    for i, game_data_str in enumerate(games["json"].iloc[start:]):
        game_data = json.loads(game_data_str)
        print(i + start, game_data["ID"], game_data["H_Team_ID"], game_data["A_Team_ID"], game_data["Date"])
        game_dir_path = f"{DATA_DIR}/games/parquet/games/{game_data['ID']}"
        if not os.path.exists(game_dir_path):
            os.mkdir(game_dir_path)
        if len([name for name in os.listdir(game_dir_path)
                if os.path.isfile(os.path.join(game_dir_path, name))]) == 5:
            continue
        for stat, function, columns, data_name in STATS:
            file_path = f"{DATA_DIR}/games/parquet/games/{game_data['ID']}/{stat}.parquet"
            if not os.path.exists(file_path):
                stat_data = function(game_data)
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
    DATA_DIR = "../../data/nba"
    DRIVER_PATH = "../other/geckodriver"

    STATS = [
        # ("box_score", get_box_score, col_names_box_score, "boxscore"),
        ("main_info", get_main_info, col_names_main_info, "home")
        # ("score_evolution", get_score_evolution, col_names_score_evolution, "game_development"),
        # ("play_by_play", get_play_by_play, col_names_play_by_play, "play_by_play"),
        # ("comparison", get_comparison, col_names_comparison, "advanced_stats")
        ]

    # get_games()
    # get_games_data()
    # join_seasons_data()
    get_venues()
