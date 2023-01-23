from json_site import get_json, get_games_data
from src.other.venues import VenueScraper


def download_games():
    codes = get_json.get_finals_codes(BASE_URL, DATA_DIR, CHROME_DRIVER_PATH, start=2022, end=2000)
    get_json.download_json_files(DATA_DIR, LEAGUE_CODE, BASE_URL_API, codes)


def get_games(ex):
    games_data = get_games_data.open_files(DATA_DIR, ex, first_season=2007, last_season=2022)
    get_games_data.save_data(DATA_DIR, games_data)


def get_venues():
    venue_scraper = VenueScraper(DATA_DIR, CHROME_DRIVER_PATH, "basketball", "arena")
    venue_scraper.get_capacity_data()
    venue_scraper.get_location_data()
    venue_scraper.merge_files()


if __name__ == "__main__":
    BASE_URL = "https://www.euroleaguebasketball.net/euroleague"
    BASE_URL_API = "https://live.euroleague.net/api"
    DATA_DIR = "../../data/euroleague"
    CHROME_DRIVER_PATH = "../other/chromedriver"
    LEAGUE_CODE = "E"

    # download_games()
    # get_games(ex=[])
    get_venues()
