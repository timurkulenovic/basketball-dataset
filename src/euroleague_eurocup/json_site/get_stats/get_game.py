import pandas as pd
import numpy as np


def get_game(data):
    header = data['Header']
    score_h, score_a = int(header["ScoreA"]), int(header["ScoreB"])
    played = score_a != 0 and score_h != 0
    href = pd.NA

    game = [header['Phase'],
            header['Round'],
            played,
            header['Date'],
            header['Hour'],
            header["TeamA"],
            header["TeamB"],
            header["ScoreA"],
            header["ScoreB"],
            href]

    return np.array([game])
