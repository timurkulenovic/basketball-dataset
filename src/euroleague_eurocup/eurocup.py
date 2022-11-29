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
    BASE_URL = "https://www.euroleaguebasketball.net/eurocup"
    BASE_URL_API = "https://live.euroleague.net/api"
    DATA_DIR = "../../data/eurocup"
    CHROME_DRIVER_PATH = "../other/chromedriver"
    LEAGUE_CODE = "U"

    #download()
    exceptions = [("2015", "13"), ("2013", "1"), ("2013", "75"), ("2008", "119"), ("2008", "90"), ("2008", "112")]
    get_games(exceptions)
