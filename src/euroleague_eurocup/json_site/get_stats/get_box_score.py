import pandas as pd
import numpy as np


def get_box_score_fields(fields_dict, type_):
    minutes, seconds = "00", "00"
    if fields_dict['Minutes'] != "DNP" and fields_dict['Minutes'] != '':
        minutes, seconds = fields_dict['Minutes'].split(":")

    fg2_a = fields_dict['FieldGoalsAttempted2']
    fg2_m = fields_dict['FieldGoalsMade2']
    fg2_perc = np.round(fg2_m / fg2_a * 100, 2) if fg2_a > 0 else pd.NA

    fg3_a = fields_dict['FieldGoalsAttempted3']
    fg3_m = fields_dict['FieldGoalsMade3']
    fg3_perc = np.round(fg3_m / fg3_a * 100, 2) if fg3_a > 0 else pd.NA

    ft_a = fields_dict['FreeThrowsAttempted']
    ft_m = fields_dict['FreeThrowsMade']
    ft_perc = np.round(ft_m / ft_a * 100, 2) if ft_a > 0 else pd.NA

    fg_a = fg2_a + fg3_a
    fg_m = fg2_m + fg3_m
    fg_perc = np.round(fg_m / fg_a * 100, 2) if fg_a > 0 else pd.NA

    fields_list = [minutes,
                   seconds,
                   fields_dict['Points'],
                   fg_m,
                   fg_a,
                   fg_perc,
                   fg2_m,
                   fg2_a,
                   fg2_perc,
                   fg3_m,
                   fg3_a,
                   fg3_perc,
                   ft_m,
                   ft_a,
                   ft_perc,
                   fields_dict['OffensiveRebounds'],
                   fields_dict['DefensiveRebounds'],
                   fields_dict['TotalRebounds'],
                   fields_dict['Assistances'],
                   fields_dict['Steals'],
                   fields_dict['Turnovers'],
                   fields_dict['BlocksFavour'],
                   fields_dict['BlocksAgainst'],
                   fields_dict['FoulsCommited'],
                   fields_dict['FoulsReceived'],
                   fields_dict['Valuation']
                   ]

    player_specific_fields = [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]
    if type_ == "Player":
        player_specific_fields = [int(fields_dict['Dorsal']),
                                  fields_dict['Player'],
                                  fields_dict['Player_ID'].strip(),
                                  bool(fields_dict['IsStarter']),
                                  bool(fields_dict['IsPlaying'])
                                  ]
    fields_list = [*player_specific_fields, *fields_list]

    return fields_list


def get_box_score(data):

    players_home = data["Boxscore"]['Stats'][0]['PlayersStats']
    box_score_players_home = [get_box_score_fields(player, "Player") for player in players_home]
    box_score_team_home = [["Team", "H", *get_box_score_fields(data["Boxscore"]['Stats'][0]['totr'], "Team")]]
    box_score_players_home = np.insert(box_score_players_home, 0, "H", axis=1)
    box_score_players_home = np.insert(box_score_players_home, 0, "Player", axis=1)

    players_away = data["Boxscore"]['Stats'][1]['PlayersStats']
    box_score_players_away = [get_box_score_fields(player, "Player") for player in players_away]
    box_score_team_away = [["Team", "A", *get_box_score_fields(data["Boxscore"]['Stats'][1]['totr'], "Team")]]
    box_score_players_away = np.insert(box_score_players_away, 0, "A", axis=1)
    box_score_players_away = np.insert(box_score_players_away, 0, "Player", axis=1)

    box_score = np.concatenate([box_score_players_home,
                                box_score_team_home,
                                box_score_players_away,
                                box_score_team_away], axis=0)

    return box_score
