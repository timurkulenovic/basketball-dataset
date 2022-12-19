from json_site import get_json, get_games_data


def download():
    get_json.create_dir(DATA_DIR)
    codes = get_json.get_finals_codes(BASE_URL, DATA_DIR, CHROME_DRIVER_PATH, start=2022, end=2000)
    get_json.download_json_files(DATA_DIR, LEAGUE_CODE, BASE_URL_API, codes)


def get_games(ex):
    games_data = get_games_data.open_files(DATA_DIR, ex, first_season=2007, last_season=2022)
    get_games_data.save_data(DATA_DIR, games_data)


if __name__ == "__main__":
    BASE_URL = "https://www.euroleaguebasketball.net/eurocup"
    BASE_URL_API = "https://live.euroleague.net/api"
    DATA_DIR = "../../data/eurocup"
    CHROME_DRIVER_PATH = "../other/chromedriver"
    LEAGUE_CODE = "U"

    # download()
    exceptions = []
    get_games(exceptions)
