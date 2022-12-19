import numpy as np
import pandas as pd


def get_score_evolution(data):
    score_evolution_data = data["Evolution"]
    score = np.array(score_evolution_data['PointsList']).T
    score_diff = np.array(score_evolution_data['ScoreDiffPerMinute']).T
    minutes = np.atleast_2d(np.array(score_evolution_data['MinutesList'])).T

    if len(minutes) + len(score) + len(score_diff) == 0:
        evolution = [[pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]]
    else:
        evolution = np.hstack((minutes, score, score_diff))

    return evolution
