from bs4 import BeautifulSoup as bs
import re
import numpy as np
import pandas as pd


def get_main_info(bs_object, game_data, BASE_URL):
    rnd = None if game_data["Round"] == "" else game_data["Round"]
    rnd = rnd.replace("F", "").replace("P", "").replace("Č", "")
    game_main_info_bs = bs_object.find("div", {"class": "mbt-v2-game-main-information"})
    if not game_main_info_bs:
        return []
    main_info_spans = game_main_info_bs.find_all("span")
    venue, attendance = None, None
    for span in main_info_spans:
        if span.find("i", {"class": "fa-globe"}):
            venue = span.text.strip()
        if span.find("i", {"class": "fa-users"}):
            attendance = span.text.strip()

    refs_bs = game_main_info_bs.next_sibling.next_sibling
    refs = [ref.strip().split("(")[0] for ref in refs_bs.text.replace("Sodniki:", "").strip().split(",")]
    if len(refs) == 2:
        refs = refs + [None]
    if len(refs) == 1:
        refs = refs + [None, None]

    result_teams_bs = bs_object.find("div", {"class": "mbt-v2-grid"})
    h_logo = result_teams_bs.find("div", {"class": "mbt-v2-game-team-logo-a"}).find("a")
    h_team_id = h_logo.get("team_id") if h_logo else None

    a_logo = result_teams_bs.find("div", {"class": "mbt-v2-game-team-logo-b"}).find("a")
    a_team_id = a_logo.get("team_id") if a_logo else None

    q_scores = [sc.text.strip().split(" : ") for sc in
                result_teams_bs.find_all("span", {"class": "mbt-v2-game-quarter-scores-score"})]

    [[h_Q1, a_Q1], [h_Q2, a_Q2], [h_Q3, a_Q3], [h_Q4, a_Q4]] = q_scores[:4]
    h_OT1, a_OT1, h_OT2, a_OT2, h_OT3, a_OT3, h_OT4, a_OT4 = None, None, None, None, None, None, None, None
    if len(q_scores) > 4:
        h_OT1, a_OT1 = q_scores[4]
    if len(q_scores) > 5:
        h_OT2, a_OT2 = q_scores[5]
    if len(q_scores) > 6:
        h_OT3, a_OT3 = q_scores[6]
    if len(q_scores) > 7:
        h_OT4, a_OT4 = q_scores[7]

    h_team_coach = game_data.get("H_Team_Coach", None)
    a_team_coach = game_data.get("A_Team_Coach", None)

    main_info = [game_data["Season"], game_data["ID"], game_data["Stage"], rnd,
                 game_data["Date"], game_data["Time"], venue, attendance,
                 *refs, game_data["H_Team"], game_data["A_Team"], h_team_id, a_team_id,
                 h_team_coach, a_team_coach,
                 game_data["H_Score"], game_data["A_Score"], h_Q1, h_Q2, h_Q3, h_Q4,
                 h_OT1, h_OT2, h_OT3, h_OT4, a_Q1, a_Q2, a_Q3, a_Q4, a_OT1, a_OT2, a_OT3, a_OT4]

    return np.array([main_info])
