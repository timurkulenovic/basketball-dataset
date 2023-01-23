import pandas as pd


def manipulate_csv():
    acb = pd.read_csv("../../data/aba/aba_games.csv")
    acb = acb.drop("Unnamed: 0", axis=1)
    acb.columns = col_names
    acb.to_csv("../../data/aba/aba_games.csv", index=False)


def month_to_number(month):
    month_dict = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }
    return month_dict[month]


col_names = [
                "Season", "Part", "Round", "Date", "Time", "Venue",
                "Attendance", "Referee1", "Referee2", "Referee3",
                "H_Team", "A_Team", "H_Team_ID", "A_Team_ID", "H_Score", "A_Score",
                "H_Q1", "H_Q2", "H_Q3", "H_Q4", "H_OT_1", "H_OT_2", "H_OT_3", "H_OT_4",
                "A_Q1", "A_Q2", "A_Q3", "A_Q4", "A_OT_1", "A_OT_2", "A_OT_3", "A_OT_4",
                "H_2FG_M", "H_2FG_A", "H_3FG_M", "H_3FG_A", "H_FT_M", "H_FT_A",
                "H_REB_O", "H_REB_D", "H_REB_T", "H_ASS", "H_ST", "H_TO", "H_BLC_FV",
                "H_BLC_AG", "H_FLS_CM", "H_FLS_RV", "H_PIR",
                "A_2FG_A", "A_2FG_M", "A_3FG_A", "A_3FG_M", "A_FT_A", "A_FT_M",
                "A_REB_O", "A_REB_D", "A_REB_T", "A_ASS", "A_ST", "A_TO", "A_BLC_FV",
                "A_BLC_AG", "A_FLS_CM", "A_FLS_RV", "A_PIR"
]
