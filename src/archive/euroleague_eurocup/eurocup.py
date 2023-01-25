import json_download as jd
import json


def download():
    jd.create_dir(DATA_DIR)
    codes = jd.get_finals_codes(BASE_URL, DATA_DIR)
    jd.download_json_files(DATA_DIR, codes)


def json_to_csv():
    with open("../../../data/basketball/eurocup_api/json/2007/1/2007_1_Points.json", 'r') as f:
        data = json.load(f)


if __name__ == "__main__":
    BASE_URL = "https://www.euroleaguebasketball.net/eurocup"
    DATA_DIR = "../../../data/basketball/eurocup_api"
    CHROME_DRIVER_PATH = "../../other/chromedriver"

    json_to_csv()