import re
import numpy as np
from bs4 import BeautifulSoup as bs


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


def get_game(bs_game, href):

    played = True

    # Game info
    _, phase, rnd = [span.text.strip() for span in bs_game.find("div", {"class": "gc-title"}).find_all("span")]

    date_loc = bs_game.find("div", {"class": "dates"})
    date, time = date_loc.find("div", {"class": "date"}).text.split(" CET: ")
    date_l = date.split(" ")
    date_string = f"{date_l[2]}/{month_to_number(date_l[0])}/{date_l[1].replace(',', '')}"
    score = bs_game.find("div", {"class": "game-score"})

    # Home team basic data
    home = score.find("div", {"class": "local"})
    h_code = re.findall("clubcode=[A-Z]+", home.find("a").get("href"))[0].replace("clubcode=", "")
    h_name = home.find("span", {"class": "name"}).text

    # Away team basic data
    away = score.find("div", {"class": "road"})
    a_name = away.find("span", {"class": "name"}).text
    a_score = away.find("span", {"class": "score"}).text

    game = [phase,
            rnd,
            played,
            date_string,
            time,
            h_name,
            a_name,
            h_code,
            a_score,
            href]

    return np.array([game])
