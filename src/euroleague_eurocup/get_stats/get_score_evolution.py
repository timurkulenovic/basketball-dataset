import numpy as np


def get_score_evolution(data):
    score_evolution_data = data["Evolution"]
    score = np.array(score_evolution_data['PointsList']).T
    score_diff = np.array(score_evolution_data['ScoreDiffPerMinute']).T
    minutes = np.atleast_2d(np.array(score_evolution_data['MinutesList'])).T
    evolution = np.hstack((minutes, score, score_diff))

    return evolution
