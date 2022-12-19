import pandas as pd
import numpy as np


def get_shots(data):
    h_id = data["Header"]["CodeTeamA"]
    points_data = data['Points']['Rows']
    if len(points_data) == 0:
        return np.array([[pd.NA for _ in range(19)]])

    df = pd.DataFrame.from_dict(points_data)
    df['TEAM'] = ["H" if team == h_id else "A" for team in df['TEAM'].str.strip()]
    df['ID_PLAYER'] = df['ID_PLAYER'].str.strip()
    df['QUARTER'] = pd.Series([(minute - 1) // 10 + 1 for minute in df['MINUTE']]).astype(str)
    df['QUARTER'] = ['OT' if q not in ["1", "2", "3", "4"] else q for q in df["QUARTER"]]

    return np.array(df)
