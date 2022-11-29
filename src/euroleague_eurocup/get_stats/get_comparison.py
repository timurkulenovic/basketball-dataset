import numpy as np


def get_comparison(data):
    comparison_data = data["Comparison"]
    shooting_graphic_data = data["ShootingGraphic"]

    comparison_columns = [
        ('DefensiveReboundsA', int),
        ('DefensiveReboundsB', int),
        ('OffensiveReboundsA', int),
        ('OffensiveReboundsB', int),
        ('TurnoversStartersA', int),
        ('TurnoversBenchA', int),
        ('TurnoversStartersB', int),
        ('TurnoversBenchB', int),
        ('StealsStartersA', int),
        ('StealsBenchA', int),
        ('StealsStartersB', int),
        ('StealsBenchB', int),
        ('AssistsStartersA', int),
        ('AssistsBenchA', int),
        ('AssistsStartersB', int),
        ('AssistsBenchB', int),
        ('PointsStartersA', int),
        ('PointsBenchA', int),
        ('PointsStartersB', int),
        ('PointsBenchB', int),
        ('maxLeadA', int),
        ('maxLeadB', int),
        ('minuteMaxLeadA', int),
        ('minuteMaxLeadB', int),
        ('puntosMaxLeadA', str),
        ('puntosMaxLeadB', str)
    ]

    shooting_graphic_columns = [
        ('FastbreakPointsA', int),
        ('FastbreakPointsB', int),
        ('TurnoversPointsA', int),
        ('TurnoversPointsB', int),
        ('SecondChancePointsA', int),
        ('SecondChancePointsB', int)
    ]

    comparison = [type_(comparison_data[col]) if comparison_data[col] else None for col, type_ in comparison_columns]
    shooting_graphic = [type_(shooting_graphic_data[col]) if shooting_graphic_data[col] else None
                        for col, type_ in shooting_graphic_columns]

    return np.array([[*comparison, *shooting_graphic]], dtype=object)
