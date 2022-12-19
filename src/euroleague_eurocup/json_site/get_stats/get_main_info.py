import pandas as pd
import numpy as np


def get_main_info(data):
    header = data['Header']
    box_score = data["Boxscore"]

    home_quarters, away_quarters = box_score['ByQuarter']

    main_info = [header['Phase'],
                 header['Round'],
                 header['Date'],
                 header['Hour'],
                 header["Stadium"],
                 box_score['Attendance'],
                 header['Referee1'],
                 header['Referee2'],
                 header['Referee3'],
                 header['TeamA'],
                 header['TeamB'],
                 header['CodeTeamA'],
                 header['CodeTeamB'],
                 box_score['Stats'][0]['Coach'],
                 box_score['Stats'][1]['Coach'],
                 int(header["ScoreA"]),
                 int(header["ScoreB"]),
                 int(home_quarters['Quarter1']),
                 int(home_quarters['Quarter2']),
                 int(home_quarters['Quarter3']),
                 int(home_quarters['Quarter4']),
                 int(home_quarters['Extra1']) if 'Extra1' in home_quarters else pd.NA,
                 int(home_quarters['Extra2']) if 'Extra2' in home_quarters else pd.NA,
                 int(home_quarters['Extra3']) if 'Extra3' in home_quarters else pd.NA,
                 int(home_quarters['Extra4']) if 'Extra4' in home_quarters else pd.NA,
                 int(home_quarters['Extra5']) if 'Extra5' in home_quarters else pd.NA,
                 int(away_quarters['Quarter1']),
                 int(away_quarters['Quarter2']),
                 int(away_quarters['Quarter3']),
                 int(away_quarters['Quarter4']),
                 int(away_quarters['Extra1']) if 'Extra1' in away_quarters else pd.NA,
                 int(away_quarters['Extra2']) if 'Extra2' in away_quarters else pd.NA,
                 int(away_quarters['Extra3']) if 'Extra3' in away_quarters else pd.NA,
                 int(away_quarters['Extra4']) if 'Extra4' in away_quarters else pd.NA,
                 int(away_quarters['Extra5']) if 'Extra5' in away_quarters else pd.NA
                 ]

    return np.array([main_info], dtype=object)
