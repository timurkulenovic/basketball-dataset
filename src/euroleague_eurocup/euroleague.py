from get_json import create_dir, get_finals_codes, download_json_files
from get_games_data import open_files, save_data


def download():
    create_dir(DATA_DIR)
    codes = get_finals_codes(BASE_URL, DATA_DIR, CHROME_DRIVER_PATH)
    download_json_files(DATA_DIR, LEAGUE_CODE, BASE_URL_API, codes)


def get_games(ex):
    games_data = open_files(DATA_DIR, ex)
    save_data(DATA_DIR, games_data)


if __name__ == "__main__":
    BASE_URL = "https://www.euroleaguebasketball.net/euroleague"
    BASE_URL_API = "https://live.euroleague.net/api"
    DATA_DIR = "../../data/euroleague"
    CHROME_DRIVER_PATH = "../other/chromedriver"
    LEAGUE_CODE = "E"

    # download()
    exceptions = [("2018", "21")]
    get_games(exceptions)
