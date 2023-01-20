# This script goes through ABA leagues seasons and writes basic info
# about games (including the game's hyperref) into a CSV.

# Each line in the output CSV consists of:
# Season, Round, Date, Time, Home team, Away team, Home score, Away score, Href


import re
import pandas as pd
import json
import numpy as np
import requests
from bs4 import BeautifulSoup as bs

from src.aba.col_names import col_names_main_info
from src.aba.col_names import col_names_play_by_play
from src.aba.col_names import col_names_box_score
from src.aba.col_names import col_names_score_evolution
from src.aba.col_names import col_names_shots

from get_stats.get_main_info import get_main_info
from get_stats.get_box_score import get_box_score
from get_stats.get_score_evolution import get_score_evolution
from get_stats.get_shots import get_shots
from get_stats.get_play_by_play import get_play_by_play

BASE_URL = "https://www.aba-liga.com"
DATA_PATH = "../../data/aba/games/parquet"


def extract_info(game):
    teams_td, score_td, date_time_td, _ = game.find_all("td")
    a = score_td.find("a")

    # Check if game was not played yet
    if a is None:
        return False

    # Get basic info
    href = a.get("href")
    team_h, team_a = [team.strip() for team in
                      teams_td.find("p", {"class": "hidden-xs"}).text.strip().split(" : ")]
    score_h, score_a = [score.replace("(*)", "") for score in score_td.text.strip().split(" : ")]
    datetime = re.sub("^\S*,", "", date_time_td.text.strip()).strip()

    # Check if game was registered as 20:0
    if int(score_h) == 20 and int(score_a) == 0 or int(score_h) == 0 and int(score_a) == 20:
        date_formatted = pd.NA
        time = pd.NA
        played = False
    else:
        played = True
        date, time, cet = datetime.split(" ")
        date_formatted = date.replace(".", "/")

    # Create game ID
    el = href.split("/")
    id_ = f"{el[5]}_{el[4]}"

    return [id_, played, date_formatted, time, team_h, team_a, score_h, score_a, href]


def get_games():
    games = []
    req_main = requests.get(f'{BASE_URL}/calendar')
    bs_main = bs(req_main.text, "html.parser")
    seasons = [(s.text.replace("Season ", "").strip(), s.get("value")) for s in
               bs_main.find("select", {"id": "season"}).find_all("option")]

    # Go through seasons
    for (season_text, season_value) in seasons:
        req_season = requests.get(f'{BASE_URL}/calendar/{season_value}')
        bs_season = bs(req_season.text, "html.parser")

        # Go through rounds
        for rnd_table in bs_season.find_all("div", {"class": "panel"}):
            rnd_text = rnd_table.find("h4", {"class": "panel-title"}).text.replace(" ", "").strip()
            stage = "Regular"

            if "Preliminary Playoff" in rnd_text:
                stage = "Preliminary Playoff"
            elif "Semifinal" in rnd_text:
                stage = "Semifinal"
            elif "Final" in rnd_text:
                stage = "Final"

            rnd_num = re.findall(r'\d+', rnd_text)
            rnd = rnd_num[0] if len(rnd_num) == 1 else pd.NA

            for game in rnd_table.find("tbody").find_all("tr"):
                game_info = extract_info(game)
                if game_info:
                    games.append([season_text, stage, rnd, *game_info])

    # Write to a file
    games_df = pd.DataFrame(data=games, columns=["Season", "Stage", "Round", "ID", "Played", "Date", "Time",
                                                 "H_Team", "A_Team", "H_Score", "A_Score", "Href"])
    games_df.to_parquet(f"{DATA_PATH}/games.parquet", index=False)


def init_games_data():
    games_data = {}
    for description, _, _ in STATS:
        games_data[description] = []
    return games_data


def get_games_data():
    games = pd.read_parquet(f"{DATA_PATH}/games.parquet")
    games['json'] = games.apply(lambda x: x.to_json(), axis=1)
    games_data = init_games_data()

    start = 0
    for i, game_data_str in enumerate(games["json"][start:]):
        game_data = json.loads(game_data_str)
        if game_data["Played"]:
            print(i + start, game_data["Href"])
            req_game = requests.get(game_data["Href"])
            bs_game = bs(req_game.text, "html.parser")
            for stat, function, columns in STATS:
                stat_data = function(bs_game, game_data)

                if len(stat_data) > 0:
                    games_data[stat].append(stat_data)

                col_names = [c for c, t in columns]
                data = np.concatenate(games_data[stat], axis=0)
                df = pd.DataFrame(data=data, columns=col_names)
                for col_name, col_type in columns:
                    df[col_name] = df[col_name].astype(col_type)
                df.to_parquet(f"{DATA_PATH}/{stat}.parquet", index=False)


if __name__ == "__main__":
    get_games()
    STATS = [
        ("main_info", get_main_info, col_names_main_info),
        ("box_score", get_box_score, col_names_box_score),
        ("score_evolution", get_score_evolution, col_names_score_evolution),
        ("shots", get_shots, col_names_shots),
        ("play_by_play", get_play_by_play, col_names_play_by_play)
        ]
    get_games_data()
