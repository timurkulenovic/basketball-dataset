from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import json
from nba_api.stats.endpoints import boxscoretraditionalv2
import requests
import time


def get_box_score(game_data):
    game_id = game_data["ID"]
    box_score_summary = json.loads(boxscoretraditionalv2.BoxScoreTraditionalV2(game_id).get_response())
    time.sleep(0.1)
    dfs = {el["name"]: pd.DataFrame(data=el["rowSet"], columns=el["headers"]) for el in box_score_summary["resultSets"]}
    dfs["PlayerStats"]["TYPE"] = "Player"
    return np.array(dfs["PlayerStats"])
