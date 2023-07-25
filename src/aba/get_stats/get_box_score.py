import numpy as np
import pandas as pd


def get_stats(bs_object, row_type):
    rows = bs_object.find("tbody").find_all("tr")
    adv_cols_exist = True if bs_object.find("td", {"class": "AdvStats"}) else False
    stats_data = []
    for row in rows:
        cols = row.find_all("td", {"class": None})

        player_number, player_name, player_id = pd.NA, pd.NA, pd.NA
        minutes_column = 2 if row_type == "Player" else 1
        if row_type == "Player":
            player_number = cols[0].text.strip()
            player_link = cols[1].find("a").get("href").split("/")
            player_name = player_link[5].replace("-", " ").title()
            player_id = player_link[2]

        minutes, seconds = [time_unit for time_unit in cols[minutes_column].text.split(":")]
        if minutes != "00" or seconds != "00":
            stats = [col.text.strip() for col in cols[minutes_column + 1:]]
            if "." in stats[-2]:
                stats[-2] = pd.NA

            adv_stats = [pd.NA, pd.NA, pd.NA]
            if adv_cols_exist:
                adv_stats_cols = row.find_all("td", {"class": "AdvStats"})
                adv_stats = [col.text.strip() for col in adv_stats_cols]
            stats = [*stats, *adv_stats]
        else:
            stats = 26 * [pd.NA]
        stats_data.append([player_number, player_name, player_id, minutes, seconds, *stats])

    return stats_data


def get_box_score(bs_object, game_data, BASE_URL):
    box_players_home_bs, box_players_away_bs = bs_object.find_all("table", {"class": "match_boxscore_team_table"})
    box_teams_bs = bs_object.find("table", {"class": "match_boxscore_teams_compare_table"})

    box_players_home = get_stats(box_players_home_bs, "Player")
    box_players_home = np.insert(box_players_home, 0, "H", axis=1)
    box_players_home = np.insert(box_players_home, 0, "Player", axis=1)

    box_players_away = get_stats(box_players_away_bs, "Player")
    box_players_away = np.insert(box_players_away, 0, "A", axis=1)
    box_players_away = np.insert(box_players_away, 0, "Player", axis=1)

    box_teams = get_stats(box_teams_bs, "Team")
    box_teams = np.insert(box_teams, 0, np.array(["H", "A"]), axis=1)
    box_teams = np.insert(box_teams, 0, "Team", axis=1)

    box_score = np.concatenate([box_players_home, box_players_away, box_teams], axis=0)
    box_score = np.insert(box_score, 0, game_data["ID"], axis=1)
    box_score = np.insert(box_score, 0, game_data["Season"], axis=1)

    return box_score
