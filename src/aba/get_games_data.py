import json

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs

from get_games import DATA_PATH

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
    BASE_URL = "https://www.aba-liga.com"
    DATA_PATH = "../../data/aba"
    STATS = [
        ("main_info", get_main_info, col_names_main_info),
        ("box_score", get_box_score, col_names_box_score),
        ("score_evolution", get_score_evolution, col_names_score_evolution),
        ("shots", get_shots, col_names_shots),
        ("play_by_play", get_play_by_play, col_names_play_by_play)
        ]
    get_games_data()
