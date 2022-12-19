import re
import numpy as np
from bs4 import BeautifulSoup as bs
import pandas as pd


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


def get_main_info(bs_game):

    _, phase, rnd = [span.text.strip() for span in bs_game.find("div", {"class": "gc-title"}).find_all("span")]
    date_loc = bs_game.find("div", {"class": "dates"})
    date, time = date_loc.find("div", {"class": "date"}).text.split(" CET: ")
    date_l = date.split(" ")
    date_string = f"{date_l[2]}/{month_to_number(date_l[0])}/{date_l[1].replace(',', '')}"
    venue = date_loc.find("span", {"class": "stadium"}).text
    score = bs_game.find("div", {"class": "game-score"})

    # Home team basic data
    home = score.find("div", {"class": "local"})
    h_code = re.findall("clubcode=[A-Z]+", home.find("a").get("href"))[0].replace("clubcode=", "")
    h_name = home.find("span", {"class": "name"}).text
    h_score = home.find("span", {"class": "score"}).text

    # Away team basic data
    away = score.find("div", {"class": "road"})
    a_code = re.findall("clubcode=[A-Z]+", away.find("a").get("href"))[0].replace("clubcode=", "")
    a_name = away.find("span", {"class": "name"}).text
    a_score = away.find("span", {"class": "score"}).text

    # Audience and referees
    attendance = bs_game.find("div", {"class": "AudienceContainer"}).text.split(": ")[1].strip()
    referees = bs_game.find("div", {"class": "RefereesContainer"}).text.strip().split(": ")[1].split("; ")
    ref1, ref2, ref3 = referees[0].replace(",", ""), referees[1].replace(",", ""), referees[2].replace(",", "")

    # Results by quarters
    quarters_bs = bs_game.find("div", {"class": "PartialsStatsByQuarterContainer"})
    h_quarter_tr, a_quarter_tr = quarters_bs.find_all("tr")[1:]
    h_quarters = [td.text.strip() for td in h_quarter_tr.find_all("td")[1:]]
    a_quarters = [td.text.strip() for td in a_quarter_tr.find_all("td")[1:]]

    # Add None for at most 4 overtimes
    h_quarters = h_quarters + ((8 - len(h_quarters)) * [pd.NA])
    a_quarters = a_quarters + ((8 - len(a_quarters)) * [pd.NA])

    # Coaches
    coaches = bs_game.find_all("div", {"class": "eu-team-stats-headcoach"})
    h_coach, a_coach = [coach.find_all("span")[1].text.strip() for coach in coaches]

    main_info = [phase,
                 rnd,
                 date_string,
                 time,
                 venue,
                 attendance,
                 ref1,
                 ref2,
                 ref3,
                 h_name,
                 a_name,
                 h_code,
                 a_code,
                 h_coach,
                 a_coach,
                 h_score,
                 a_score,
                 *h_quarters,
                 *a_quarters,
                 ]

    return np.array([main_info], dtype=object)
