import re
import pandas as pd
import numpy as np


def get_box_score_fields(row, type_):
    cells = [cell.text.strip() for cell in row.find_all("td")]
    num, name, time, pts, fg2, fg3, ft, r_off, r_def, r_tot, ass, st, to, fv, ag, cm, rv, val = cells

    minutes, seconds = 0, 0
    if time != "DNP":
        minutes, seconds = [int(unit) for unit in time.split(":")]

    fg2_a, fg2_m, fg2_perc = 0, 0, pd.NA
    if fg2 != "" and fg2 != "-":
        fg2_m, fg2_a = [int(unit) for unit in fg2.split("/")]
        fg2_perc = np.round(fg2_m / fg2_a * 100, 2)

    fg3_a, fg3_m, fg3_perc = 0, 0, pd.NA
    if fg3 != "" and fg3 != "-":
        fg3_m, fg3_a = [int(unit) for unit in fg3.split("/")]
        fg3_perc = np.round(fg3_m / fg3_a * 100, 2)

    ft_a, ft_m, ft_perc = 0, 0, pd.NA
    if ft != "" and ft != "-":
        ft_m, ft_a = [int(unit) for unit in ft.split("/")]
        ft_perc = np.round(ft_m / ft_a * 100, 2)

    fg_a = fg2_a + fg3_a
    fg_m = fg2_m + fg3_m
    fg_perc = np.round(fg_m / fg_a * 100, 2) if fg_a > 0 else pd.NA

    points = int(pts) if pts != "" and pts != "-" else 0
    off_reb = int(r_off) if r_off != "" and r_off != "-" else 0
    def_reb = int(r_def) if r_def != "" and r_def != "-" else 0
    tot_reb = int(r_tot) if r_tot != "" and r_tot != "-" else 0
    assists = int(ass) if ass != "" and ass != "-" else 0
    steals = int(st) if st != "" and st != "-" else 0
    turnovers = int(to) if to != "" and to != "-" else 0
    blocks_for = int(fv) if fv != "" and fv != "-" else 0
    blocks_against = int(ag) if ag != "" and ag != "-" else 0
    fouls_cm = int(cm) if cm != "" and cm != "-" else 0
    fouls_rv = int(rv) if rv != "" and rv != "-" else 0
    valuation = int(val) if val != "" and val != "-" else 0

    fields_list = [minutes,
                   seconds,
                   points,
                   fg_m,
                   fg_a,
                   fg_perc,
                   fg2_m,
                   fg2_a,
                   fg2_perc,
                   fg3_m,
                   fg3_a,
                   fg3_perc,
                   ft_m,
                   ft_a,
                   ft_perc,
                   off_reb,
                   def_reb,
                   tot_reb,
                   assists,
                   steals,
                   turnovers,
                   blocks_for,
                   blocks_against,
                   fouls_cm,
                   fouls_rv,
                   valuation
                   ]

    player_specific_fields = [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]
    if type_ == "Player":
        player_name_a = row.find("td", {"class": "PlayerContainer"}).find("a")
        id_ = re.findall("pcode=\S+&", player_name_a.get("href"))[0].replace("pcode=", "").replace("&", "")
        a_cls = player_name_a.get("class")
        player_specific_fields = [int(num),
                                  name,
                                  f"P{id_}",
                                  True if (a_cls and a_cls[0] == "PlayerStartFive") else False,
                                  pd.NA     # no data about player finishing the game
                                  ]
    fields_list = [*player_specific_fields, *fields_list]
    return fields_list


def get_box_score(bs_game):
    h_box_score = bs_game.find("div", {"class": "LocalClubStatsContainer"}).find("table")
    box_score_players_home = [get_box_score_fields(p, "Player") for p in h_box_score.find_all("tr")[2:-3]]
    box_score_team_home = [["Team", "H", *get_box_score_fields(h_box_score.find("tfoot").
                                                               find("tr", {"class": "TotalFooter"}), "Team")]]
    box_score_players_home = np.insert(box_score_players_home, 0, "H", axis=1)
    box_score_players_home = np.insert(box_score_players_home, 0, "Player", axis=1)

    a_box_score = bs_game.find("div", {"class": "RoadClubStatsContainer"}).find("table")
    box_score_players_away = [get_box_score_fields(p, "Player") for p in a_box_score.find_all("tr")[2:-3]]
    box_score_team_away = [["Team", "A", *get_box_score_fields(a_box_score.find("tfoot").
                                                               find("tr", {"class": "TotalFooter"}), "Team")]]
    box_score_players_away = np.insert(box_score_players_away, 0, "A", axis=1)
    box_score_players_away = np.insert(box_score_players_away, 0, "Player", axis=1)

    box_score = np.concatenate([box_score_players_home,
                                box_score_team_home,
                                box_score_players_away,
                                box_score_team_away], axis=0)

    return box_score
