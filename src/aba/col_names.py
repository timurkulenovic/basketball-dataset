import pandas as pd


col_names_games = [
    ("SEASON", pd.StringDtype()),
    ("STAGE", pd.StringDtype()),
    ("ROUND", pd.Int64Dtype()),
    ("ID", pd.StringDtype()),
    ("PLAYED", pd.BooleanDtype()),
    ("DATE", pd.StringDtype()),
    ("TIMR", pd.StringDtype()),
    ("H_TEAM", pd.StringDtype()),
    ("A_TEAM", pd.StringDtype()),
    ("H_SCORE", pd.Int64Dtype()),
    ("A_SCORE", pd.Int64Dtype()),
    ("HREF", pd.StringDtype())
]

col_names_main_info = [
    ("SEASON", pd.StringDtype()),
    ("GAME_ID", pd.StringDtype()),
    ("STAGE", pd.StringDtype()),
    ("ROUND", pd.Int64Dtype()),
    ("DATE", pd.StringDtype()),
    ("TIME", pd.StringDtype()),
    ("VENUE", pd.StringDtype()),
    ("ATTENDANCE", pd.Int64Dtype()),
    ("REFEREE1", pd.StringDtype()),
    ("REFEREE2", pd.StringDtype()),
    ("REFEREE3", pd.StringDtype()),
    ("H_TEAM", pd.StringDtype()),
    ("A_TEAM", pd.StringDtype()),
    ("H_TEAM_ID", pd.StringDtype()),
    ("A_TEAM_ID", pd.StringDtype()),
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
    ("A_Q1", pd.Int64Dtype()),
    ("A_Q2", pd.Int64Dtype()),
    ("A_Q3", pd.Int64Dtype()),
    ("A_Q4", pd.Int64Dtype()),
    ("A_OT_1", pd.Int64Dtype()),
    ("A_OT_2", pd.Int64Dtype()),
    ("A_OT_3", pd.Int64Dtype()),
    ("A_OT_4", pd.Int64Dtype())
]

col_names_box_score = [
    ("SEASON", pd.StringDtype()),
    ("GAME_ID", pd.StringDtype()),
    ("TYPE", pd.StringDtype()),
    ("TEAM", pd.StringDtype()),
    ("PLAYER_NUMBER", pd.Int64Dtype()),
    ("PLAYER_NAME", pd.StringDtype()),
    ("PLAYER_ID", pd.Int64Dtype()),
    ("MINUTES", pd.Int64Dtype()),
    ("SECONDS", pd.Int64Dtype()),
    ("POINTS", pd.Int64Dtype()),
    ("FG_PERC", pd.Float64Dtype()),
    ("FG2_M", pd.Int64Dtype()),
    ("FG2_A", pd.Int64Dtype()),
    ("FG2_PERC", pd.Float64Dtype()),
    ("FG3_M", pd.Int64Dtype()),
    ("FG3_A", pd.Int64Dtype()),
    ("FG3_PERC", pd.Float64Dtype()),
    ("FT_M", pd.Int64Dtype()),
    ("FT_A", pd.Int64Dtype()),
    ("FT_PERC", pd.Float64Dtype()),
    ("REB_O", pd.Int64Dtype()),
    ("REB_D", pd.Int64Dtype()),
    ("REB_T", pd.Int64Dtype()),
    ("ASS", pd.Int64Dtype()),
    ("ST", pd.Int64Dtype()),
    ("TO", pd.Int64Dtype()),
    ("BLC_FV", pd.Int64Dtype()),
    ("BLC_AG", pd.Int64Dtype()),
    ("FLS_CM", pd.Int64Dtype()),
    ("FLS_RV", pd.Int64Dtype()),
    ("PLUS_MINUS", pd.Int64Dtype()),
    ("VAL", pd.Int64Dtype()),
    ("PTS_PAINT", pd.Int64Dtype()),
    ("PTS_2ND_CHANCE", pd.Int64Dtype()),
    ("PTS_FAST_BREAK", pd.Int64Dtype())
]

col_names_shots = [
    ("SEASON", pd.StringDtype()),
    ("GAME_ID", pd.StringDtype()),
    ("TEAM", pd.StringDtype()),
    ("X", pd.Float64Dtype()),
    ("Y", pd.Float64Dtype()),
    ("MADE", pd.BooleanDtype()),
    ("PLAYER_ID", pd.Int64Dtype()),
    ("PLAYER_NAME", pd.StringDtype())
]

col_names_score_evolution = [
    ("SEASON", pd.StringDtype()),
    ("GAME_ID", pd.StringDtype()),
    ("MINUTE", pd.Int64Dtype()),
    ("H_SCORE", pd.Int64Dtype()),
    ("A_SCORE", pd.Int64Dtype())
]

col_names_play_by_play = [
    ("SEASON", pd.StringDtype()),
    ("GAME_ID", pd.StringDtype()),
    ("QUARTER", pd.StringDtype()),
    ("MINUTES", pd.Int64Dtype()),
    ("SECONDS", pd.Int64Dtype()),
    ("TEAM", pd.StringDtype()),
    ("H_SCORE", pd.Int64Dtype()),
    ("A_SCORE", pd.Int64Dtype()),
    ("PLAYER_NUMBER", pd.Int64Dtype()),
    ("PLAYER_ID", pd.Int64Dtype()),
    ("PLAYER_NAME", pd.StringDtype()),
    ("PLAY_TYPE", pd.StringDtype()),
    ("PLAY_NOTE", pd.StringDtype()),
    ("MISSING_DATA", pd.BooleanDtype())
]
