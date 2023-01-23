from bs4 import BeautifulSoup as bs
import requests
from scrape.other.selenium_init import selenium_driver
import json
import time
import os


def create_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def confirm_cookies(driver):
    bs_game_center_cookies = bs(driver.page_source, "html.parser")
    if bs_game_center_cookies.find("div", {"class": "ot-sdk-row"}):
        driver.find_element_by_xpath(f"//button[@id='onetrust-accept-btn-handler']").click()
        time.sleep(1)


def get_finals_codes(start=2021, end=2007):
    filepath = os.path.join(DATA_DIR, "final_codes.json")
    code_finals = {}
    if os.path.exists(filepath):
        file = open(filepath)
        code_finals = json.load(file)
    if not os.path.exists(filepath):
        driver = selenium_driver(BASE_URL, CHROME_DRIVER_PATH)
        driver.get(f"{BASE_URL}/game-center")
        time.sleep(2)
        confirm_cookies(driver)
        for season_year in range(start, end-1, -1):
            driver.get(f'{BASE_URL}/game-center/?round=100&season=U{season_year}')
            time.sleep(10)
            bs_round = bs(driver.page_source, "html.parser")
            link = bs_round.find_all("a", {"class": "game-card-view_linkWrap__u3Tea"})[-1].get("href")
            code_final = int(link.split("/")[-2])
            code_finals[season_year] = code_final
        driver.close()
        with open(filepath, "w") as file:
            json.dump(code_finals, file)
    return code_finals


def download_json_files(code_finals):
    if not os.path.exists(os.path.join(DATA_DIR, "json")):
        os.makedirs(os.path.join(DATA_DIR, "json"))
    for season_year, final_code in code_finals.items():
        print(season_year)
        if not os.path.exists(os.path.join(DATA_DIR, "json", season_year)):
            os.makedirs(os.path.join(DATA_DIR, "json", season_year))
        for code in range(final_code, 0, -1):
            print(f"\t{code}", end=" ")
            if not os.path.exists(os.path.join(DATA_DIR, "json", season_year, str(code))):
                print("Downloading...")
                os.makedirs(os.path.join(DATA_DIR, "json", season_year, str(code)))
                filenames = ["PlaybyPlay", "Boxscore", "Points", "Header", "Evolution", "ShootingGraphic", "Comparison"]
                for filename in filenames:
                    response = requests.get(f"https://live.euroleague.net/api/{filename}?gamecode={code}&seasoncode=E{season_year}")
                    try:
                        json_response = response.json()
                        filepath = os.path.join(DATA_DIR, "json", season_year, str(code), f"{season_year}_{code}_{filename}.json")
                        with open(filepath, "w") as file:
                            json.dump(json_response, file)
                    except ValueError:
                        pass
            else:
                print("Already downloaded")
            # Delete directory if empty
            if not os.listdir(os.path.join(DATA_DIR, "json", season_year, str(code))):
                os.rmdir(os.path.join(DATA_DIR, "json", season_year, str(code)))


if __name__ == "__main__":
    BASE_URL = "https://www.euroleaguebasketball.net/eurocup"
    DATA_DIR = "../../../data/basketball/eurocup_api"
    CHROME_DRIVER_PATH = "../../other/chromedriver"

    create_dir()
    codes = get_finals_codes()
    download_json_files(codes)
