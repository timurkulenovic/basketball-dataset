from bs4 import BeautifulSoup as bs
import requests
from src.other.selenium_init import selenium_driver
import json
import time
import os


def confirm_cookies(driver):
    bs_game_center_cookies = bs(driver.page_source, "html.parser")
    if bs_game_center_cookies.find("div", {"class": "ot-sdk-row"}):
        driver.find_element_by_xpath(f"//button[@id='onetrust-accept-btn-handler']").click()
        time.sleep(1)


def get_finals_codes(BASE_URL, DATA_DIR, CHROME_PATH, start, end):
    filepath = os.path.join(DATA_DIR, "games", "json", "final_codes", "final_codes.json")
    if os.path.exists(filepath):
        with open(filepath) as f:
            code_finals = json.load(f)
        return code_finals

    code_finals = {}
    if os.path.exists(filepath):
        file = open(filepath)
        code_finals = json.load(file)
    if not os.path.exists(filepath):
        driver = selenium_driver(BASE_URL, CHROME_PATH)
        driver.get(f"{BASE_URL}/game-center")
        time.sleep(2)
        confirm_cookies(driver)
        for season_year in range(start, end-1, -1):
            driver.get(f'{BASE_URL}/game-center/?round=100&season=E{season_year}')
            time.sleep(5)
            bs_round = bs(driver.page_source, "html.parser")
            link = bs_round.find_all("a", {"class": "game-card-view_linkWrap__u3Tea"})[-1].get("href")
            code_final = int(link.split("/")[-2])
            code_finals[season_year] = code_final
        driver.close()
        with open(filepath, "w") as file:
            json.dump(code_finals, file)
    return code_finals


def download_json_files(DATA_DIR, league_code, BASE_URL_API, code_finals):
    if not os.path.exists(os.path.join(DATA_DIR, "games", "json")):
        os.makedirs(os.path.join(DATA_DIR, "games", "json"))
    for season_year, final_code in code_finals.items():
        print(season_year)
        if not os.path.exists(os.path.join(DATA_DIR, "games", "json", "seasons", season_year)):
            os.makedirs(os.path.join(DATA_DIR, "games", "json", "seasons", season_year))
        for code in range(final_code, 0, -1):
            print(f"\t{code}", end=" ")
            if not os.path.exists(os.path.join(DATA_DIR, "games", "json", "seasons", season_year, str(code))):
                print("Downloading...")
                os.makedirs(os.path.join(DATA_DIR, "games", "json", "seasons", season_year, str(code)))
                filenames = ["PlaybyPlay", "Boxscore", "Points", "Header", "Evolution", "ShootingGraphic", "Comparison"]
                for filename in filenames:
                    response = requests.get(f"{BASE_URL_API}/{filename}?gamecode={code}&seasoncode="
                                            f"{league_code}{season_year}")
                    try:
                        json_response = response.json()
                        filepath = os.path.join(DATA_DIR, "games", "json", "seasons", season_year, str(code),
                                                f"{season_year}_{code}_{filename}.json")
                        with open(filepath, "w") as file:
                            json.dump(json_response, file)
                    except ValueError:
                        pass
            else:
                print("Already downloaded")
            # Delete directory if empty
            if not os.listdir(os.path.join(DATA_DIR, "games", "json", "seasons", season_year, str(code))):
                os.rmdir(os.path.join(DATA_DIR, "games", "json", "seasons", season_year, str(code)))
