import numpy as np


def get_comparison(bs_object, game_data, BASE_URL):
    table = bs_object.find("table", {"id": "mbt-v2-game-starter-bench-comparison-table"})
    if not table:
        return []
    table_td = [td.text.strip() for td in table.find("tbody").find_all("td")]
    n = int(len(table_td) / 4)
    table_td_2d = [table_td[i:i + n] for i in range(0, len(table_td), n)]

    h_starters_min, h_bench_min, a_starters_min, a_bench_min = table_td_2d[0][1], table_td_2d[1][1],\
        table_td_2d[2][1], table_td_2d[3][1]
    h_starters_reb, h_bench_reb, a_starters_reb, a_bench_reb = table_td_2d[0][10], table_td_2d[1][10],\
        table_td_2d[2][10], table_td_2d[3][10]
    h_starters_assists, h_bench_assists, a_starters_assists, a_bench_assists = table_td_2d[0][11], table_td_2d[1][11],\
        table_td_2d[2][11], table_td_2d[3][11]
    h_starters_fouls, h_bench_fouls, a_starters_fouls, a_bench_fouls = table_td_2d[0][12], table_td_2d[1][12],\
        table_td_2d[2][12], table_td_2d[3][12]
    h_starters_turnovers, h_bench_turnovers, a_starters_turnovers, a_bench_turnovers = table_td_2d[0][14], table_td_2d[1][14],\
        table_td_2d[2][14], table_td_2d[3][14]
    h_starters_steals, h_bench_steals, a_starters_steals, a_bench_steals = table_td_2d[0][15], table_td_2d[1][15],\
        table_td_2d[2][15], table_td_2d[3][15]
    h_starters_eff, h_bench_eff, a_starters_eff, a_bench_eff = table_td_2d[0][18], table_td_2d[1][18],\
        table_td_2d[2][18], table_td_2d[3][18]
    h_starters_pts, h_bench_pts, a_starters_pts, a_bench_pts = table_td_2d[0][19], table_td_2d[1][19],\
        table_td_2d[2][19], table_td_2d[3][19]

    various_stats_table = bs_object.find("table", {"id": "mbt-v2-game-various-stats-table"}).find("tbody")
    rows = various_stats_table.find_all("tr")
    if len(rows) > 13:
        _, h_possessions, a_possessions = [td.text.strip() for td in rows[5].find_all("td")]
        _, h_highest_lead, a_highest_lead = [td.text.strip().split(" ")[0] for td in rows[9].find_all("td")]
        _, h_pts_paint, a_pts_paint = [td.text.strip() for td in rows[10].find_all("td")]
        _, h_pts_fast_break, a_pts_fast_break = [td.text.strip() for td in rows[11].find_all("td")]
        _, h_pts_second_chance, a_pts_second_chance = [td.text.strip() for td in rows[12].find_all("td")]
        _, h_pts_turnovers, a_pts_turnovers = [td.text.strip() for td in rows[13].find_all("td")]
    else:
        _, h_possessions, a_possessions = [td.text.strip() for td in rows[5].find_all("td")]
        _, h_highest_lead, a_highest_lead = [td.text.strip().split(" ")[0] for td in rows[9].find_all("td")]
        _, h_pts_paint, a_pts_paint = [td.text.strip() for td in rows[10].find_all("td")]
        h_pts_fast_break, a_pts_fast_break = None, None
        h_pts_second_chance, a_pts_second_chance = None, None
        h_pts_turnovers, a_pts_turnovers = None, None

    comparison = [game_data["Season"], game_data["ID"],
                  h_starters_min, h_bench_min, a_starters_min, a_bench_min,
                  h_starters_reb, h_bench_reb, a_starters_reb, a_bench_reb,
                  h_starters_assists, h_bench_assists, a_starters_assists, a_bench_assists,
                  h_starters_fouls, h_bench_fouls, a_starters_fouls, a_bench_fouls,
                  h_starters_turnovers, h_bench_turnovers, a_starters_turnovers, a_bench_turnovers,
                  h_starters_steals, h_bench_steals, a_starters_steals, a_bench_steals,
                  h_starters_eff, h_bench_eff, a_starters_eff, a_bench_eff,
                  h_starters_pts, h_bench_pts, a_starters_pts, a_bench_pts,
                  h_possessions, a_possessions,
                  h_highest_lead, a_highest_lead,
                  h_pts_paint, a_pts_paint,
                  h_pts_fast_break, a_pts_fast_break,
                  h_pts_second_chance, a_pts_second_chance,
                  h_pts_turnovers, a_pts_turnovers]

    return np.array([comparison])
