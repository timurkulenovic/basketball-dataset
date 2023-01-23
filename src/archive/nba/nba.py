from nba_api.stats.endpoints import leaguegamefinder, boxscoresummaryv2
import time
from scrape.basketball.helpers import col_names, month_to_number
import pandas as pd
import os
import json

WIKI_URL = "https://en.wikipedia.org"
seasons_info = []

if not os.path.exists('../../../data/basketball/nba'):
    os.makedirs('../../../data/basketball/nba')


def parse_start_end(date_str):
    beg_str, end_str = date_str.split(" – ")
    end_str = end_str.replace(" (Playoffs)", "")
    end_str = end_str.replace(" (Finals)", "")
    end_list = end_str.replace(",", "").split(" ")
    print(end_list)
    end = f"{end_list[2]}-{month_to_number(end_list[0])}-{end_list[1]}"
    if "," in beg_str:
        beg_list = beg_str.replace(",", "").split(" ")
        beg = f"{beg_list[2]}-{month_to_number(beg_list[0])}-{beg_list[1]}"
    else:
        beg_list = beg_str.split(" ")
        beg = f"{end_list[2]}-{month_to_number(beg_list[0])}-{beg_list[1]}"
    return end, beg


games_data = []
seasons = [f"{year}-{str(year + 1)[2:]}" for year in range(2000, 2001)]
parts = ["Regular Season", "Playoffs"]

for season in seasons:
    for part in parts:
        games = leaguegamefinder.LeagueGameFinder(league_id_nullable="00",
                                                  season_nullable=season,
                                                  season_type_nullable=part).get_data_frames()[0]

        print(season, part)
        for game_id in games.GAME_ID.unique():
            games_with_id = games[games.GAME_ID == game_id]
            matchup = games_with_id[games_with_id['MATCHUP'].str.contains("vs.")].iloc[0]["MATCHUP"]
            h_team_abb, a_team_abb = matchup.split(" vs. ")

            h_team_data = games_with_id[games_with_id["TEAM_ABBREVIATION"] == h_team_abb].iloc[0]
            a_team_data = games_with_id[games_with_id["TEAM_ABBREVIATION"] == a_team_abb].iloc[0]

            # box score data
            h_team, a_team = h_team_data["TEAM_NAME"], a_team_data["TEAM_NAME"]
            h_score, a_score = h_team_data["PTS"], a_team_data["PTS"]
            h_fgm, a_fgm = h_team_data["FGM"], a_team_data["FGM"]
            h_fga, a_fga = h_team_data["FGA"], a_team_data["FGA"]
            h_3pm, a_3pm = h_team_data["FG3M"], a_team_data["FG3M"]
            h_3pa, a_3pa = h_team_data["FG3A"], a_team_data["FG3A"]
            h_2pm, a_2pm = h_fgm - h_3pm, a_fgm - a_3pm
            h_2pa, a_2pa = h_fga - h_3pa, a_fga - a_3pa
            h_fta, a_fta = h_team_data["FTA"], a_team_data["FTA"]
            h_ftm, a_ftm = h_team_data["FTM"], a_team_data["FTM"]
            h_reb_d, a_reb_d = h_team_data["DREB"], a_team_data["DREB"]
            h_reb_o, a_reb_o = h_team_data["OREB"], a_team_data["OREB"]
            h_reb_tot, a_reb_tot = h_team_data["REB"], a_team_data["REB"]
            h_ast, a_ast = h_team_data["AST"], a_team_data["AST"]
            h_stl, a_stl = h_team_data["STL"], a_team_data["STL"]
            h_to, a_to = h_team_data["TOV"], a_team_data["TOV"]
            h_blc_fv, a_blc_fv = h_team_data["BLK"], a_team_data["BLK"]
            h_blc_ag, a_blc_ag = a_blc_fv, h_blc_fv
            h_fls_cm, a_fls_cm = h_team_data["PF"], a_team_data["PF"]
            h_fls_rv, a_fls_rv = a_fls_cm, h_fls_cm
            h_pir = h_score + h_reb_tot + h_ast + h_stl + h_blc_fv + h_fls_rv - (h_fga - h_fgm) - (h_fta - h_fta) - h_to - h_blc_ag - h_fls_cm
            a_pir = a_score + a_reb_tot + a_ast + a_stl + a_blc_fv + a_fls_rv - (a_fga - a_fgm) - (a_fta - a_fta) - a_to - a_blc_ag - a_fls_cm

            # points by quarters
            box = json.loads(boxscoresummaryv2.BoxScoreSummaryV2(game_id).get_response())
            linescore = [el for el in box["resultSets"] if el["name"] == "LineScore"][0]
            linescore_df = pd.DataFrame(data=linescore["rowSet"], columns=linescore["headers"])
            h_team_q = linescore_df[linescore_df["TEAM_ABBREVIATION"] == h_team_abb].iloc[0]
            a_team_q = linescore_df[linescore_df["TEAM_ABBREVIATION"] == a_team_abb].iloc[0]

            h_q1, h_q2, h_q3, h_q4 = h_team_q["PTS_QTR1"], h_team_q["PTS_QTR2"], h_team_q["PTS_QTR3"], h_team_q["PTS_QTR4"]
            h_ot1, h_ot2, h_ot3, h_ot4 = h_team_q["PTS_OT1"], h_team_q["PTS_OT2"],  h_team_q["PTS_OT3"], h_team_q["PTS_OT4"]
            a_q1, a_q2, a_q3, a_q4 = a_team_q["PTS_QTR1"], a_team_q["PTS_QTR2"], a_team_q["PTS_QTR3"], a_team_q["PTS_QTR4"]
            a_ot1, a_ot2, a_ot3, a_ot4 = a_team_q["PTS_OT1"],  a_team_q["PTS_OT2"],  a_team_q["PTS_OT3"], a_team_q["PTS_OT4"]

            season_str = f"{season.split('-')[0]}/20{season.split('-')[1]}"
            game_info = [el for el in box["resultSets"] if el["name"] == "GameInfo"][0]
            att = game_info["rowSet"][0][1]
            game_summary = [el for el in box["resultSets"] if el["name"] == "GameSummary"][0]
            date = game_summary["rowSet"][0][0].split("T")[0].replace("-", "/")
            officials_summary = [el for el in box["resultSets"] if el["name"] == "Officials"][0]
            ref1, ref2, ref3 = None, None, None
            if len(officials_summary["rowSet"]) == 3:
                ref1, ref2, ref3 = [f"{off[1]} {off[2]}" for off in officials_summary["rowSet"]]
            game_time = None
            venue = None
            rnd = None

            game_data = [season_str, part, rnd, date, game_time, venue, att, ref1, ref2, ref3,
                         h_team, a_team, h_team_abb, a_team_abb, h_score, a_score,
                         h_q1, h_q2, h_q3, h_q4, h_ot1, h_ot2, h_ot3, h_ot4,
                         a_q1, a_q2, a_q3, a_q4, a_ot1, a_ot2, a_ot3, a_ot4,
                         h_2pm, h_2pa, h_3pm, h_3pa, h_ftm, h_fta, h_reb_o, h_reb_d, h_reb_tot,
                         h_ast, h_stl, h_to, h_blc_fv, h_blc_ag, h_fls_cm, h_fls_rv, h_pir,
                         a_2pm, a_2pa, a_3pm, a_3pa, a_ftm, a_fta, a_reb_o, a_reb_d, a_reb_tot,
                         a_ast, a_stl, a_to, a_blc_fv, a_blc_ag, a_fls_cm, a_fls_rv, a_pir]

            print(game_data)
            games_data.append(game_data)
            df_nba = pd.DataFrame(data=games_data, columns=col_names)
            df_nba.to_csv("../../data/basketball/nba/nba_games.csv", index=False)
            time.sleep(1)
