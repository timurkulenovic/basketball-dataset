import pandas as pd


col_names_games = [
    ("SEASON", pd.StringDtype()),
    ("GAME_ID", pd.StringDtype()),
    ("GAME_ID_IN_SEASON", pd.StringDtype()),
    ("STAGE", pd.StringDtype()),
    ("ROUND", pd.Int64Dtype()),
    ("PLAYED", pd.BooleanDtype()),
    ("DATE", pd.StringDtype()),
    ("TIME", pd.StringDtype()),
    ("H_TEAM", pd.StringDtype()),
    ("A_TEAM", pd.StringDtype()),
    ("H_SCORE", pd.Int64Dtype()),
    ("A_SCORE", pd.Int64Dtype()),
    ("HREF", pd.StringDtype())
]


col_names_main_info = [
    ("SEASON", pd.StringDtype()),
    ("GAME_ID", pd.StringDtype()),
    ("GAME_ID_IN_SEASON", pd.StringDtype()),
    ("STAGE", pd.StringDtype()),
    ("ROUND", pd.Int64Dtype()),
    ("DATE", pd.StringDtype()),
    ("TIME", pd.StringDtype()),
    ("VENUE", pd.StringDtype()),
    ("ATTENDANCE", pd.Int64Dtype()),
    ("REFEREE1", pd.StringDtype()),
    ("REFEREE2", pd.StringDtype()),
    ("REFEREE3", pd.StringDtype()),
    ("H_Team", pd.StringDtype()),
    ("A_Team", pd.StringDtype()),
    ("H_Team_ID", pd.StringDtype()),
    ("A_Team_ID", pd.StringDtype()),
    ("H_TEAM_COACH", pd.StringDtype()),
    ("A_TEAM_COACH", pd.StringDtype()),
    ("H_SCORE", pd.Int64Dtype()),
    ("A_SCORE", pd.Int64Dtype()),
    ("H_Q1", pd.Int64Dtype()),
    ("H_Q2", pd.Int64Dtype()),
    ("H_Q3", pd.Int64Dtype()),
    ("H_Q4", pd.Int64Dtype()),
    ("H_OT_1", pd.Int64Dtype()),
    ("H_OT_2", pd.Int64Dtype()),
    ("H_OT_3", pd.Int64Dtype()),
    ("H_OT_4", pd.Int64Dtype()),
    ("H_OT_5", pd.Int64Dtype()),
    ("A_Q1", pd.Int64Dtype()),
    ("A_Q2", pd.Int64Dtype()),
    ("A_Q3", pd.Int64Dtype()),
    ("A_Q4", pd.Int64Dtype()),
    ("A_OT_1", pd.Int64Dtype()),
    ("A_OT_2", pd.Int64Dtype()),
    ("A_OT_3", pd.Int64Dtype()),
    ("A_OT_4", pd.Int64Dtype()),
    ("A_OT_5", pd.Int64Dtype())
]


col_names_box_score = [
    ("SEASON", pd.StringDtype()),
    ("GAME_ID", pd.StringDtype()),
    ("GAME_ID_IN_SEASON", pd.StringDtype()),
    ("TYPE", pd.StringDtype()),
    ("TEAM", pd.StringDtype()),
    ("PLAYER_NUMBER", pd.Int64Dtype()),
    ("PLAYER_NAME", pd.StringDtype()),
    ("PLAYER_ID", pd.StringDtype()),
    ("PLAYER_STARTER", pd.BooleanDtype()),
    ("PLAYER_FINISHED", pd.BooleanDtype()),
    ("MINUTES", pd.Int64Dtype()),
    ("SECONDS", pd.Int64Dtype()),
    ("POINTS", pd.Int64Dtype()),
    ("FG_M", pd.Int64Dtype()),
    ("FG_A", pd.Int64Dtype()),
    ("FG_PERC", pd.Float64Dtype()),
    ("FG2_M", pd.Int64Dtype()),
    ("FG2_A", pd.Int64Dtype()),
    ("FG2_PERC", pd.Float64Dtype()),
    ("FG3_M", pd.Int64Dtype()),
    ("FG3_A", pd.Int64Dtype()),
    ("FG3_PERC", pd.Float64Dtype()),
    ("FT_M", pd.Int64Dtype()),
    ("FT_A", pd.Int64Dtype()),
    ("FT_Perc", pd.Float64Dtype()),
    ("REB_OFF", pd.Int64Dtype()),
    ("REB_DEF", pd.Int64Dtype()),
    ("REB_TOT", pd.Int64Dtype()),
    ("ASS", pd.Int64Dtype()),
    ("ST", pd.Int64Dtype()),
    ("TO", pd.Int64Dtype()),
    ("BLC_FV", pd.Int64Dtype()),
    ("BLC_AG", pd.Int64Dtype()),
    ("FLS_CM", pd.Int64Dtype()),
    ("FLS_RV", pd.Int64Dtype()),
    ("VAL", pd.Int64Dtype())
]

col_names_comparison = [
    ("SEASON", pd.StringDtype()),
    ("GAME_ID", pd.StringDtype()),
    ("GAME_ID_IN_SEASON", pd.StringDtype()),
    ("REB_DEF_H", pd.Int64Dtype()),
    ("REB_DEF_A", pd.Int64Dtype()),
    ("REB_OFF_H", pd.Int64Dtype()),
    ("REB_OFF_A", pd.Int64Dtype()),
    ("TO_STARTERS_H", pd.Int64Dtype()),
    ("TO_BENCH_H", pd.Int64Dtype()),
    ("TO_STARTERS_A", pd.Int64Dtype()),
    ("TO_BENCH_A", pd.Int64Dtype()),
    ("STEALS_STARTERS_H", pd.Int64Dtype()),
    ("STEALS_BENCH_H", pd.Int64Dtype()),
    ("STEALS_STARTERS_A", pd.Int64Dtype()),
    ("STEALS_BENCH_A", pd.Int64Dtype()),
    ("ASSISTS_STARTERS_H", pd.Int64Dtype()),
    ("ASSISTS_BENCH_H", pd.Int64Dtype()),
    ("ASSISTS_STARTERS_A", pd.Int64Dtype()),
    ("ASSISTS_BENCH_A", pd.Int64Dtype()),
    ("POINTS_STARTERS_H", pd.Int64Dtype()),
    ("PTS_BENCH_H", pd.Int64Dtype()),
    ("PTS_STARTERS_A", pd.Int64Dtype()),
    ("PTS_BENCH_A", pd.Int64Dtype()),
    ("MAX_LEAD_H", pd.Int64Dtype()),
    ("MAX_LEAD_A", pd.Int64Dtype()),
    ("MAX_LEAD_MINUTE_H", pd.Int64Dtype()),
    ("MAX_LEAD_MINUTE_A", pd.Int64Dtype()),
    ("MAX_LEAD_RESULT_H", pd.StringDtype()),
    ("MAX_LEAD_RESULT_A", pd.StringDtype()),
    ("FASTBREAK_PTS_H", pd.Int64Dtype()),
    ("FASTBREAK_PTS_A", pd.Int64Dtype()),
    ("TO_PTS_H", pd.Int64Dtype()),
    ("TO_PTS_A", pd.Int64Dtype()),
    ("SECOND_CHANCE_PTS_H", pd.Int64Dtype()),
    ("SECOND_CHANCE_PTS_A", pd.Int64Dtype()),
]

col_names_shots = [
    ("SEASON", pd.StringDtype()),
    ("GAME_ID", pd.StringDtype()),
    ("GAME_ID_IN_SEASON", pd.StringDtype()),
    ("NUM_ANOT", pd.StringDtype()),
    ("Team", pd.StringDtype()),
    ("Player_ID", pd.StringDtype()),
    ("Player_Name", pd.StringDtype()),
    ("ID_ACTION", pd.StringDtype()),
    ("ACTION", pd.StringDtype()),
    ("POINTS", pd.Int64Dtype()),
    ("X", pd.Int64Dtype()),
    ("Y", pd.Int64Dtype()),
    ("ZONE", pd.StringDtype()),
    ("FASTBREAK", pd.Int64Dtype()),
    ("SECOND_CHANCE", pd.Int64Dtype()),
    ("PTS_OFF_TO", pd.Int64Dtype()),
    ("MINUTE", pd.Int64Dtype()),
    ("TIME", pd.StringDtype()),
    ("PTS_H", pd.Int64Dtype()),
    ("PTS_A", pd.Int64Dtype()),
    ("UTC", pd.StringDtype()),
    ("QUARTER", pd.StringDtype())
]

col_names_score_evolution = [
    ("SEASON", pd.StringDtype()),
    ("GAME_ID", pd.StringDtype()),
    ("GAME_ID_IN_SEASON", pd.StringDtype()),
    ("MINUTE", pd.Int64Dtype()),
    ("SCORE_H", pd.Int64Dtype()),
    ("SCORE_A", pd.Int64Dtype()),
    ("DIFF_H", pd.Int64Dtype()),
    ("DIFF_A", pd.Int64Dtype())
]

col_names_play_by_play = [
    ("SEASON", pd.StringDtype()),
    ("GAME_ID", pd.StringDtype()),
    ("GAME_ID_IN_SEASON", pd.StringDtype()),
    ("TYPE", pd.Int64Dtype()),
    ("NUM_OF_PLAY", pd.Int64Dtype()),
    ("TEAM", pd.StringDtype()),
    ("PLAYER_ID", pd.StringDtype()),
    ("PLAY_TYPE", pd.StringDtype()),
    ("PLAYER_NAME", pd.StringDtype()),
    ("TEAM_NAME", pd.StringDtype()),
    ("PLAYER_NUMBER", pd.StringDtype()),
    ("MINUTE", pd.Int64Dtype()),
    ("TIME", pd.StringDtype()),
    ("SCORE_H", pd.Int64Dtype()),
    ("SCORE_A", pd.Int64Dtype()),
    ("COMMENT", pd.StringDtype()),
    ("PLAY_INFO", pd.StringDtype()),
    ("QUARTER", pd.StringDtype())
]
