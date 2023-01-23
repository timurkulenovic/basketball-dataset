from bs4 import BeautifulSoup as bs
import requests
import re
from scrape.basketball.helpers import month_to_number
from scrape.basketball.helpers import col_names
import pandas as pd
import os

BASE_URL = "https://www.eurocupbasketball.com"
games_data = []
if not os.path.exists('../../data/eurocup'):
    os.makedirs('../../data/eurocup')

req_main = requests.get(f'{BASE_URL}/eurocup/games/results')
bs_main = bs(req_main.text, "html.parser")
season_sel = bs_main.find_all("div", {"class": "styled-select"})[0]

for season_opt in season_sel.find("select").find_all("option"):
    season = season_opt.text.replace("-", "/")
    req_season = requests.get(f'{BASE_URL}{season_opt.get("value")}')
    bs_season = bs(req_season.text, "html.parser")
    season_part_sel = bs_season.find_all("div", {"class": "styled-select"})[1]

    for season_part_opt in season_part_sel.find("select").find_all("option"):
        season_part = season_part_opt.text.replace("-", "/")
        req_season_part = requests.get(f'{BASE_URL}{season_part_opt.get("value")}')
        bs_part = bs(req_season_part.text, "html.parser")
        round_sel = bs_part.find_all("div", {"class": "styled-select"})[2]

        for round_opt in round_sel.find("select").find_all("option"):
            rnd = round_opt.text
            req_rnd = requests.get(f'{BASE_URL}{round_opt.get("value")}')
            bs_rnd = bs(req_rnd.text, "html.parser")
            games = bs_rnd.find_all("div", {"class": "game played"})

            for game in games:
                req_game = requests.get(f'{BASE_URL}{game.find("a").get("href")}')
                bs_game = bs(req_game.text, "html.parser")

                # Game info
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
                ref1, ref2, ref3 = referees[0].replace(",", ""), referees[1].replace(",", ""), referees[2].replace(",",
                                                                                                                   "")

                # Results by quarters
                quarters_bs = bs_game.find("div", {"class": "PartialsStatsByQuarterContainer"})
                h_quarter_tr, a_quarter_tr = quarters_bs.find_all("tr")[1:]
                h_quarters = [td.text.strip() for td in h_quarter_tr.find_all("td")[1:]]
                a_quarters = [td.text.strip() for td in a_quarter_tr.find_all("td")[1:]]

                # Add None for at most 4 overtimes
                h_quarters = h_quarters + ((8 - len(h_quarters)) * [None])
                a_quarters = a_quarters + ((8 - len(a_quarters)) * [None])

                # Box score Home team
                h_stats_td = bs_game.find("div", {"class": "LocalClubStatsContainer"}).find("table").find("tfoot").find("tr", {"class": "TotalFooter"}).find_all("td")[4:]
                h_stats = [td.text.split("/") if "/" in td.text else td.text for td in h_stats_td]
                h_stats = h_stats[0] + h_stats[1] + h_stats[2] + h_stats[3:]

                # Box score Away team
                a_stats_td = bs_game.find("div", {"class": "RoadClubStatsContainer"}).find("table").find("tfoot").find("tr", {"class": "TotalFooter"}).find_all("td")[4:]
                a_stats = [td.text.split("/") if "/" in td.text else td.text for td in a_stats_td]
                a_stats = a_stats[0] + a_stats[1] + a_stats[2] + a_stats[3:]

                # Gather all the data
                game_row = [
                    season, season_part, rnd,
                    date_string, time, venue,
                    attendance, ref1, ref2, ref3,
                    h_name, a_name, h_code, a_code,
                    h_score, a_score, *h_quarters,
                    *a_quarters, *h_stats, *a_stats
                ]
                print(game_row)
                games_data.append(game_row)

    # Save data
    df_eurocup = pd.DataFrame(data=games_data, columns=col_names)
    df_eurocup.to_csv("../../../data/eurocup/eurocup_games.csv", index=False)
