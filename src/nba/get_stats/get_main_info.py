from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import json
from nba_api.stats.endpoints import boxscoresummaryv2, scoreboardv2, teamdetails, commonteamroster
from nba_api.live.nba.endpoints import boxscore
import requests
import time


def get_main_info(game_data):
    game_id = game_data["ID"]
    box_score_summary = json.loads(boxscoresummaryv2.BoxScoreSummaryV2(game_id).get_response())
    time.sleep(0.05)
    dfs = {el["name"]: pd.DataFrame(data=el["rowSet"], columns=el["headers"]) for el in box_score_summary["resultSets"]}

    try:
        boxscore_game = boxscore.BoxScore(game_id)
        time.sleep(0.05)
        arena_dict = boxscore_game.arena.get_dict()
        game_dict = boxscore_game.game.get_dict()
        venue = f"{arena_dict['arenaName'], arena_dict['arenaCity'], arena_dict['arenaState']}"
        time_ = game_dict['gameTimeUTC'].split("T")[1].replace("Z", "")
    except:
        website = requests.get(f"https://www.nba.com/game/{game_id}").text
        website_bs = BeautifulSoup(website, "html.parser").find("script", {"type": "application/ld+json"})
        if website_bs is None:
            return []

        website_data = json.loads(website_bs.text)
        time_ = website_data['startDate'].split("T")[1].replace("Z", "")
        venue = website_data['location']['name']

    attendance = dfs["GameInfo"].iloc[0]["ATTENDANCE"]
    officials = 4 * [None]
    if dfs["Officials"].shape[0] > 0:
        officials = [f"{official['FIRST_NAME']} {official['LAST_NAME']}" for i, official in dfs["Officials"].iterrows()]
        officials = officials[:4] if len(officials) > 4 else officials
        officials = [*officials, None, None] if len(officials) == 2 else officials
        officials = [*officials, None] if len(officials) == 3 else officials
    h_team_q = dfs["LineScore"][dfs["LineScore"]["TEAM_ABBREVIATION"]
                                # .str.replace('NOK', 'NOH')
                                .str.replace("PHO", "PHX")
                                .str.replace("PHL", "PHI")
                                .str.replace("SAN", "SAS")
                                .str.replace("UTH", "UTA")
                                .str.replace("GOS", "GSW") == game_data["H_Team_ID"]].iloc[0]
    a_team_q = dfs["LineScore"][dfs["LineScore"]["TEAM_ABBREVIATION"]
                                # .str.replace('NOK', 'NOH')
                                .str.replace("PHO", "PHX")
                                .str.replace("PHL", "PHI")
                                .str.replace("SAN", "SAS")
                                .str.replace("UTH", "UTA")
                                .str.replace("GOS", "GSW") == game_data["A_Team_ID"]].iloc[0]

    h_Q1, h_Q2, h_Q3, h_Q4 = h_team_q["PTS_QTR1"], h_team_q["PTS_QTR2"], h_team_q["PTS_QTR3"], h_team_q["PTS_QTR4"]
    h_OT1, h_OT2, h_OT3, h_OT4 = h_team_q["PTS_OT1"], h_team_q["PTS_OT2"], h_team_q["PTS_OT3"], h_team_q["PTS_OT4"]
    a_Q1, a_Q2, a_Q3, a_Q4 = a_team_q["PTS_QTR1"], a_team_q["PTS_QTR2"], a_team_q["PTS_QTR3"], a_team_q["PTS_QTR4"]
    a_OT1, a_OT2, a_OT3, a_OT4 = a_team_q["PTS_OT1"], a_team_q["PTS_OT2"], a_team_q["PTS_OT3"], a_team_q["PTS_OT4"]

    main_info = [game_data["Season"], game_data["ID"], game_data["Stage"],
                 game_data["Date"], time_, venue, attendance,
                 *officials, game_data["H_Team"], game_data["A_Team"], game_data["H_Team_ID"], game_data["A_Team_ID"],
                 None, None, game_data["H_Score"], game_data["A_Score"],
                 h_Q1, h_Q2, h_Q3, h_Q4, h_OT1, h_OT2, h_OT3, h_OT4, a_Q1, a_Q2, a_Q3, a_Q4, a_OT1, a_OT2, a_OT3, a_OT4]
    return np.array([main_info])
