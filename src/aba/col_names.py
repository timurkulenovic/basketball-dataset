import pandas as pd


col_names_games = [
    ("Season", pd.StringDtype()),
    ("Stage", pd.StringDtype()),
    ("Round", pd.Int64Dtype()),
    ("ID", pd.StringDtype()),
    ("Played", pd.BooleanDtype()),
    ("Date", pd.StringDtype()),
    ("Time", pd.StringDtype()),
    ("H_Team", pd.StringDtype()),
    ("A_Team", pd.StringDtype()),
    ("H_Score", pd.Int64Dtype()),
    ("A_Score", pd.Int64Dtype()),
    ("Href", pd.StringDtype())
]

col_names_main_info = [
    ("Season", pd.StringDtype()),
    ("Game_ID", pd.StringDtype()),
    ("Stage", pd.StringDtype()),
    ("Round", pd.Int64Dtype()),
    ("Date", pd.StringDtype()),
    ("Time", pd.StringDtype()),
    ("Venue", pd.StringDtype()),
    ("Attendance", pd.Int64Dtype()),
    ("Referee1", pd.StringDtype()),
    ("Referee2", pd.StringDtype()),
    ("Referee3", pd.StringDtype()),
    ("H_Team", pd.StringDtype()),
    ("A_Team", pd.StringDtype()),
    ("H_Team_ID", pd.StringDtype()),
    ("A_Team_ID", pd.StringDtype()),
    ("H_Score", pd.Int64Dtype()),
    ("A_Score", pd.Int64Dtype()),
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
    ("Season", pd.StringDtype()),
    ("Game_ID", pd.StringDtype()),
    ("Type", pd.StringDtype()),
    ("Team", pd.StringDtype()),
    ("Player_Number", pd.Int64Dtype()),
    ("Player_Name", pd.StringDtype()),
    ("Player_ID", pd.Int64Dtype()),
    ("Minutes", pd.Int64Dtype()),
    ("Seconds", pd.Int64Dtype()),
    ("Points", pd.Int64Dtype()),
    ("FG_Perc", pd.Float64Dtype()),
    ("FG2_M", pd.Int64Dtype()),
    ("FG2_A", pd.Int64Dtype()),
    ("FG2_Perc", pd.Float64Dtype()),
    ("FG3_M", pd.Int64Dtype()),
    ("FG3_A", pd.Int64Dtype()),
    ("FG3_Perc", pd.Float64Dtype()),
    ("FT_M", pd.Int64Dtype()),
    ("FT_A", pd.Int64Dtype()),
    ("FT_Perc", pd.Float64Dtype()),
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
    ("Plus_Minus", pd.Int64Dtype()),
    ("Val", pd.Int64Dtype()),
    ("Pts_Paint", pd.Int64Dtype()),
    ("Pts_2nd_Chance", pd.Int64Dtype()),
    ("Pts_Fast_Break", pd.Int64Dtype())
]

col_names_shots = [
    ("Season", pd.StringDtype()),
    ("Game_ID", pd.StringDtype()),
    ("Team", pd.StringDtype()),
    ("X", pd.Float64Dtype()),
    ("Y", pd.Float64Dtype()),
    ("Made", pd.BooleanDtype()),
    ("Player_ID", pd.Int64Dtype()),
    ("Player_Name", pd.StringDtype())
]

col_names_score_evolution = [
    ("Season", pd.StringDtype()),
    ("Game_ID", pd.StringDtype()),
    ("Minute", pd.Int64Dtype()),
    ("H_Score", pd.Int64Dtype()),
    ("A_Score", pd.Int64Dtype())
]

col_names_play_by_play = [
    ("Season", pd.StringDtype()),
    ("Game_ID", pd.StringDtype()),
    ("Quarter", pd.StringDtype()),
    ("Clock_Minutes", pd.Int64Dtype()),
    ("Clock_Seconds", pd.Int64Dtype()),
    ("Team", pd.StringDtype()),
    ("H_Score", pd.Int64Dtype()),
    ("A_Score", pd.Int64Dtype()),
    ("Player_Number", pd.Int64Dtype()),
    ("Player_ID", pd.Int64Dtype()),
    ("Player_Name", pd.StringDtype()),
    ("Play_Type", pd.StringDtype()),
    ("Play_Note", pd.StringDtype()),
    ("Missing_Data", pd.BooleanDtype())
]
