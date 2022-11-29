# This script goes through ABA leagues seasons and writes basic info
# about games (including the game's hyperref) into a CSV.

# Each line in the output CSV consists of:
# Season, Round, Date, Time, Home team, Away team, Home score, Away score, Href

from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd

BASE_URL = "https://www.aba-liga.com"
DATA_PATH = "../../data/aba"


def extract_info(game):
    teams_td, score_td, date_time_td, _ = game.find_all("td")
    a = score_td.find("a")

    # Check if game was not played yet
    if a is None:
        return False

    # Get basic info
    href = a.get("href")
    team_h, team_a = [team.strip() for team in
                      teams_td.find("p", {"class": "hidden-xs"}).text.strip().split(" : ")]
    score_h, score_a = [score.replace("(*)", "") for score in score_td.text.strip().split(" : ")]
    datetime = re.sub("^\S*,", "", date_time_td.text.strip()).strip()

    # Check if game was registered as 20:0
    if int(score_h) == 20 and int(score_a) == 0 or int(score_h) == 0 and int(score_a) == 20:
        date_formatted = pd.NA
        time = pd.NA
        played = False
    else:
        played = True
        date, time, cet = datetime.split(" ")
        date_formatted = date.replace(".", "/")

    # Create game ID
    el = href.split("/")
    id_ = f"{el[5]}_{el[4]}"

    return [id_, played, date_formatted, time, team_h, team_a, score_h, score_a, href]


def get_games():
    games = []
    req_main = requests.get(f'{BASE_URL}/calendar')
    bs_main = bs(req_main.text, "html.parser")
    seasons = [(s.text.replace("Season ", "").strip(), s.get("value")) for s in
               bs_main.find("select", {"id": "season"}).find_all("option")]

    # Go through seasons
    for (season_text, season_value) in seasons:
        req_season = requests.get(f'{BASE_URL}/calendar/{season_value}')
        bs_season = bs(req_season.text, "html.parser")

        # Go through rounds
        for rnd_table in bs_season.find_all("div", {"class": "panel"}):
            rnd_text = rnd_table.find("h4", {"class": "panel-title"}).text.replace(" ", "").strip()
            stage = "Regular"

            if "Preliminary Playoff" in rnd_text:
                stage = "Preliminary Playoff"
            elif "Semifinal" in rnd_text:
                stage = "Semifinal"
            elif "Final" in rnd_text:
                stage = "Final"

            rnd_num = re.findall(r'\d+', rnd_text)
            rnd = rnd_num[0] if len(rnd_num) == 1 else pd.NA

            for game in rnd_table.find("tbody").find_all("tr"):
                game_info = extract_info(game)
                if game_info:
                    games.append([season_text, stage, rnd, *game_info])

    # Write to a file
    games_df = pd.DataFrame(data=games, columns=["Season", "Stage", "Round", "ID", "Played", "Date", "Time",
                                                 "H_Team", "A_Team", "H_Score", "A_Score", "Href"])
    games_df.to_parquet(f"{DATA_PATH}/games.parquet", index=False)


if __name__ == "__main__":
    get_games()
