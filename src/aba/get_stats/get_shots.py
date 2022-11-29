import requests
import json
import pandas as pd
from games import BASE_URL
import numpy as np


def get_shots(bs_object, game_data):
    s_id, g_id = game_data["ID"].split("_")
    res = requests.get(f"{BASE_URL}/live-match/rezultati-1718/create_shooting_chart.php?id={g_id}&sez={s_id}&lea=1")
    shots_json = json.loads(res.text)
    if len(shots_json) == 0:
        return []

    shots_df = pd.DataFrame(shots_json)
    shots_df["ekipa"] = ["H" if team == 1 else "A" for team in shots_df["ekipa"]]
    shots_df["koordinata_uspeh"] = [True if made == "1" else False for made in shots_df["koordinata_uspeh"]]

    shots = np.array(shots_df)
    shots = np.insert(shots, 0, game_data["ID"], axis=1)
    shots = np.insert(shots, 0, game_data["Season"], axis=1)
    return shots
