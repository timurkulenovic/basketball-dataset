import os
import json
import pandas as pd
import numpy as np

from get_stats.get_game import get_game
from get_stats.get_main_info import get_main_info
from get_stats.get_box_score import get_box_score
from get_stats.get_comparison import get_comparison
from get_stats.get_score_evolution import get_score_evolution
from get_stats.get_shots import get_shots
from get_stats.get_play_by_play import get_play_by_play

from col_names import col_names_games
from col_names import col_names_main_info
from col_names import col_names_box_score
from col_names import col_names_comparison
from col_names import col_names_score_evolution
from col_names import col_names_shots
from col_names import col_names_play_by_play


JSON_STATS = [
    "Header",
    "Boxscore",
    "Comparison",
    "Evolution",
    "PlaybyPlay",
    "Points",
    "ShootingGraphic"
]


OUTPUT_STATS = [
    ("games", col_names_games, get_game),
    ("main_info", col_names_main_info, get_main_info),
    ("box_score", col_names_box_score, get_box_score),
    ("comparison", col_names_comparison, get_comparison),
    ("score_evolution", col_names_score_evolution, get_score_evolution),
    ("shots", col_names_shots, get_shots),
    ("play_by_play", col_names_play_by_play, get_play_by_play)
]


def extract_data(games_data, game_data, year, game_id_s):
    game_id = f"{year}_{game_id_s}"
    season = f"{year}/{int(year) + 1}"
    score_h, score_a = int(game_data["Header"]["ScoreA"]), int(game_data["Header"]["ScoreB"])
    played = score_a != 0 and score_h != 0

    for stat, columns, function in OUTPUT_STATS:
        if not played and stat != "games":
            continue
        stat_data = function(game_data)
        n_repeat = len(stat_data)
        stat_data = np.hstack((np.repeat([[season, game_id, game_id_s]], n_repeat, axis=0), stat_data))
        games_data[stat].append(stat_data)


def init_all_games_data():
    games_data = {}
    for stat, col_names, function in OUTPUT_STATS:
        games_data[stat] = []
    return games_data


def open_files(DATA_DIR, exceptions):
    games_data = init_all_games_data()
    # Go through seasons
    for year in os.listdir(os.path.join(DATA_DIR, "json", "seasons")):
        if not year.startswith('.'):
            print(year)
            # Go through games in a season
            for game_id in os.listdir(os.path.join(DATA_DIR, "json", "seasons", year)):
                if not game_id.startswith('.'):
                    # Check if game is in the exceptions
                    if (str(year), str(game_id)) not in exceptions:
                        game_data = {}
                        for stat in JSON_STATS:
                            path = os.path.join(DATA_DIR, "json", "seasons", year,
                                                game_id, f"{year}_{game_id}_{stat}.json")
                            with open(path, 'r') as f:
                                game_data[stat] = json.load(f)
                        extract_data(games_data, game_data, year, game_id)
    return games_data


def save_data(DATA_DIR, games_data):
    for stat, columns, function in OUTPUT_STATS:
        stat_data = np.concatenate(games_data[stat], axis=0)
        col_names = [c for c, t in columns]
        df = pd.DataFrame(data=stat_data, columns=col_names)
        for col_name, col_type in columns:
            df[col_name] = df[col_name].astype(col_type)
        df.to_parquet(f"{DATA_DIR}/{stat}.parquet", index=False)
