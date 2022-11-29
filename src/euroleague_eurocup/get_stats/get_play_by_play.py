import pandas as pd
import numpy as np


def get_pbp_df(quarter_data, h_id, quarter):
    if len(quarter_data) == 0:
        return []
    df = pd.DataFrame.from_dict(quarter_data)
    df['CODETEAM'] = ["H" if team == h_id else "A" for team in df['CODETEAM'].str.strip()]
    df['PLAYER_ID'] = df['PLAYER_ID'].str.strip()
    df['QUARTER'] = quarter
    return np.array(df, dtype=object)


def get_play_by_play(data):
    h_id = data["Header"]["CodeTeamA"]
    pbp_data = data['PlaybyPlay']

    quarter_1_df = get_pbp_df(pbp_data['FirstQuarter'], h_id, "1")
    quarter_2_df = get_pbp_df(pbp_data['SecondQuarter'], h_id, "2")
    quarter_3_df = get_pbp_df(pbp_data['ThirdQuarter'], h_id, "3")
    quarter_4_df = get_pbp_df(pbp_data['ForthQuarter'], h_id, "4")

    extra_time = pbp_data["ExtraTime"]
    extra_time_df = get_pbp_df(pbp_data['ExtraTime'], h_id, "OT") if extra_time and len(extra_time) > 0 else []

    dfs = [quarter_1_df, quarter_2_df, quarter_3_df, quarter_4_df, extra_time_df]
    pbp_data = [df for df in dfs if len(df) > 0]
    pbp = np.concatenate(pbp_data, axis=0) if len(pbp_data) > 0 else np.array([[]], dtype=object)
    return pbp
