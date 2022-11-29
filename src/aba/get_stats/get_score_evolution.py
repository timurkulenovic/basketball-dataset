import requests
import json
import pandas as pd
import numpy as np
from games import BASE_URL


def get_score_evolution(bs_object, game_data):
    s_id, g_id = game_data["ID"].split("_")
    res = requests.get(f"{BASE_URL}/live-match/rezultati-1718/create_json.php?id={g_id}&sez={s_id}&lea=1")
    try:
        scores_json = json.loads(res.text)
    except json.decoder.JSONDecodeError:
        return []
    scores = np.array(pd.DataFrame(scores_json))
    scores = np.insert(scores, 0, game_data["ID"], axis=1)
    scores = np.insert(scores, 0, game_data["Season"], axis=1)
    return scores
