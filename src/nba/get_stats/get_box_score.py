import numpy as np
import pandas as pd
import re


def get_box_score(bs_game, game_data, BASE_URL):
    box_score = []
    table = bs_game.find("table", {"id": "mbt-v2-game-boxscore-table"})
    if not table:
        return []
    rows = table.find("tbody").find_all("tr")
    home_team = True
    for row in rows:
        row_class = row.get("class")
        if row_class and row_class[0] == "mbt-v2-table-secondary-thead":
            continue

        cols = [el.text.strip() for el in row.find_all("td")]
        delimiter = "/" if "Vsote" in cols[0] else "-"
        total_row = True if "Vsote" in cols[0] else False
        team_row = True if "Ekipa" in cols[0] else False
        coach_row = True if "Trener" in cols[0] else False

        if coach_row:
            coach = cols[0].replace("Trener:", "").strip()
            if home_team:
                game_data["H_Team_Coach"] = coach
                home_team = False
            else:
                game_data["A_Team_Coach"] = coach
            continue

        if len(cols) == 21:
            [
                name, minutes, two_point, two_point_perc, three_point, three_point_perc,
                ft, ft_perc, off_reb, def_reb, tot_reb, assists, comm_foul, rv_foul, turnovers,
                steals, blocks_fv, blocks_ag, eff, plus_minus, points
            ] = cols
        else:
            [
                name, minutes, two_point, two_point_perc, three_point, three_point_perc, fg, fg_perc,
                ft, ft_perc, off_reb, def_reb, tot_reb, assists, comm_foul, rv_foul, turnovers,
                steals, blocks_fv, blocks_ag, eff, plus_minus, points
            ] = cols

        if total_row:
            type_ = "Total"
            name = ""
        elif team_row:
            type_ = "Team"
            name = ""
        else:
            type_ = "Player"
            name = re.sub(r'[!#\d*\n+$]', '', name)

        minutes_played = 0 if minutes == "-" or minutes == "" else int(minutes.split(":")[0])
        seconds_played = 0 if minutes == "-" or minutes == "" else int(minutes.split(":")[1])

        two_points_att = 0 if two_point == "" else int(two_point.split(delimiter)[0])
        two_points_made = 0 if two_point == "" else int(two_point.split(delimiter)[1])
        two_points_perc = 100 * two_points_made / two_points_att if two_points_att > 0 else None

        three_points_att = 0 if three_point == "" else int(three_point.split(delimiter)[0])
        three_points_made = 0 if three_point == "" else int(three_point.split(delimiter)[1])
        three_points_perc = 100 * three_points_made / three_points_att if three_points_att > 0 else None

        ft_att = 0 if ft == "" else int(ft.split(delimiter)[0])
        ft_made = 0 if ft == "" else int(ft.split(delimiter)[1])
        ft_perc = 100 * ft_made / ft_att if ft_att > 0 else None

        other_stats = [points, off_reb, def_reb, tot_reb, assists, steals, turnovers, blocks_fv, blocks_ag,
                       comm_foul, rv_foul, plus_minus, eff]
        other_stats_cleaned = [0 if stat == "" else int(stat) for stat in other_stats]

        player_number = None
        player_id = None

        team = game_data["H_Team"] if home_team else game_data["A_Team"]
        box_score_line = [game_data["Season"], game_data["ID"], type_, team, player_number, name,
                          player_id, minutes_played, seconds_played, other_stats_cleaned[0],
                          two_points_made, two_points_att, two_points_perc, three_points_made,
                          three_points_att, three_points_perc, ft_att, ft_made, ft_perc, *other_stats_cleaned[1:]]
        box_score.append(box_score_line)

    return np.array(box_score)
