from bs4 import BeautifulSoup as bs
import requests
import re
import time
import pandas as pd
import numpy as np
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrape.other.selenium_init import selenium_driver
from selenium.webdriver.common.keys import Keys
from scrape.basketball.helpers import col_names


BASE_URL = "https://www.kzs.si/"


def create_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def get_hrefs(bs_page, season, stage):
    schedule = bs_page.find("table", {"id": "mbt-v2-schedule-table"})
    if schedule:
        round_ = [r.find("td").text.strip() for r in schedule.find_all("tr")]
        hrefs = [s.find("a").get("href") for s in schedule.find_all("td", {"class": "mbt-v2-schedule-table-result-column"})]
        return [[season, stage, rnd, href] for rnd, href in zip(round_, hrefs)]
    return []


def get_play_by_play(d):
    d.find_element_by_xpath(f"//div[@data-name='play_by_play']").click()
    time.sleep(1)
    bs_play_by_play = bs(d.page_source, "html.parser")
    rows = bs_play_by_play.find("table", {"class": "mbt-v2-table mbt-v2-game-play-by-play-table"}).find(
        "tbody").find_all("tr")
    part = 1
    for row in rows:
        td = row.find_all("td")
        if len(td) > 1:
            clock, res, _, action = [td_i.text.strip() for td_i in td]
            action = action.replace("/a", "")
            action = action.split("\n")
            if len(action) == 3:
                action = action[2]
            else:
                action = action[0]
            player = None
            if "je" in action:
                player, action = action.split(" je ")
                player = player.split(") ")[1].strip()
            acted_on = None
            if "na (" in action:
                action, acted_on = action.split(" na ")
                acted_on = acted_on.split(") ")[1]

            h_points, a_points = None, None
            if len(res) > 0:
                h_points, a_points = [int(p) for p in res.split(":")]

            minutes, sec = [int(t) for t in clock.split(":")]
            minutes_quarter = int(minutes) % 10

            new_row = [part, clock, minutes_quarter, sec, h_points, a_points, action, player, acted_on]
        else:
            action = None
            if "Minuta odmora" in td[0].text:
                action = "Timeout"
            if "Konec četrtine" in td[0].text:
                part += 1
                action = "Part ends"
            if "Konec tekme" in td[0].text:
                part += 1
                action = "Game ends"
            new_row = 6 * [None] + [action] + 2 * [None]

        print(new_row)


def get_games_data(d):
    df_hrefs = pd.read_csv(f"{DATA_DIR}/game_hrefs.csv")
    get_game_data(d, "https://www.kzs.si/incl?id=114&game_id=5523079&league_id=undefined&season_id=122569")


def box_score_cell_clean():
    pass


def get_box_score(d):
    d.find_element_by_xpath(f"//div[@data-name='boxscore']").click()
    time.sleep(2)
    bs_box_score = bs(d.page_source, "html.parser")
    rows = bs_box_score.find("table", {"id": "mbt-v2-game-boxscore-table"}).find(
        "tbody").find_all("tr")
    for row in rows:
        row_class = row.get("class")
        if row_class and row_class[0] == "mbt-v2-table-secondary-thead":
            continue

        cols = [el.text.strip() for el in row.find_all("td")]
        delimiter = "/" if "Vsote" in cols[0] else "-"
        total_row = True if "Vsote" in cols[0] else False
        team_row = True if "Ekipa" in cols[0] else False
        coach_row = True if "Trener" in cols[0] else False

        if coach_row:
            coach = cols[0].replace("Trener:", "").strip()
            print(coach)
            continue

        [
            name, minutes, two_point, two_point_perc, three_point, three_point_perc, fg, fg_perc,
            ft, ft_perc, off_reb, def_reb, tot_reb, assists, comm_foul, rv_foul, turnovers,
            steals, blocks_fv, blocks_ag, eff, plus_minus, points
        ] = cols

        if total_row:
            name = "Total"
        elif team_row:
            name = "Team"
        else:
            name = re.sub(r'[!#\d*\n+$]', '', name)

        minutes_played = 0 if minutes == "-" or minutes == "" else int(minutes.split(":")[0])
        seconds_played = 0 if minutes == "-" or minutes == "" else int(minutes.split(":")[1])

        two_points_att = 0 if two_point == "" else int(two_point.split(delimiter)[0])
        two_points_made = 0 if two_point == "" else int(two_point.split(delimiter)[1])

        three_points_att = 0 if three_point == "" else int(three_point.split(delimiter)[0])
        three_points_made = 0 if three_point == "" else int(three_point.split(delimiter)[1])

        ft_att = 0 if ft == "" else int(ft.split(delimiter)[0])
        ft_made = 0 if ft == "" else int(ft.split(delimiter)[1])

        other_stats = [def_reb, off_reb, tot_reb, assists, comm_foul, rv_foul, turnovers,
                       steals, blocks_fv, blocks_ag, eff, plus_minus, points]
        other_stats_cleaned = [0 if stat == "" else int(stat) for stat in other_stats]

        player = [name, minutes_played, seconds_played, two_points_att, two_points_made, three_points_att,
                  three_points_made, ft_att, ft_made, *other_stats_cleaned]

        print(player)


def get_game_info(d):
    game_info_bs = bs(d.page_source, "html.parser")
    game_main_info_bs = game_info_bs.find("div", {"class": "mbt-v2-game-main-information"})
    game_main_info = [info.text.strip() for info in game_main_info_bs.find_all("span")]
    date, g_time, venue, attendance, tv = game_main_info
    date = date.replace(".", "/")

    refs_bs = game_main_info_bs.next_sibling.next_sibling
    refs = [ref.strip().split("(")[0] for ref in refs_bs.text.replace("Sodniki:", "").strip().split(",")]

    result_teams_bs = game_info_bs.find("div", {"class": "mbt-v2-grid"})
    h_team = result_teams_bs.find("div", {"class": "mbt-v2-game-team-logo-a"}).find("a").get("alt")
    a_team = result_teams_bs.find("div", {"class": "mbt-v2-game-team-logo-b"}).find("a").get("alt")

    h_score, a_score = [res.text.strip() for res in result_teams_bs.find_all("div", {"class": "mbt-v2-game-team-score"})]

    q_scores = [sc.text.strip().split(" : ") for sc in
                result_teams_bs.find_all("span", {"class": "mbt-v2-game-quarter-scores-score"})]

    [[h_Q1, a_Q1], [h_Q2, a_Q2], [h_Q3, a_Q3], [h_Q4, h_Q4]] = q_scores[:4]
    h_OT1, a_OT1, h_OT2, a_OT2, h_OT3, a_OT3, h_OT4, a_OT4 = None, None, None, None, None, None, None, None
    if len(q_scores) > 4:
        h_OT1, a_OT1 = q_scores[4]
    if len(q_scores) > 5:
        h_OT2, a_OT2 = q_scores[5]
    if len(q_scores) > 6:
        h_OT3, a_OT3 = q_scores[6]
    if len(q_scores) > 7:
        h_OT4, a_OT4 = q_scores[7]


def get_game_data(d, link):
    d.get(link)
    time.sleep(2)
    # get_game_info(d)
    # get_play_by_play(d)
    get_box_score(d)


def get_all_games(d):
    all_games = []
    time.sleep(3)
    bs_main = bs(d.page_source, "html.parser")
    seasons = [(opt.text.strip(), opt.get("value")) for opt in
               bs_main.find("select", {"id": "33-303-filter-season"}).find_all("option")]

    # Go through all seasons
    for i, (season_text, season_value) in enumerate(seasons):
        season_str = season_text.replace("-", "/")
        print(season_str)
        d.find_element_by_xpath(f"//select[@id='33-303-filter-season']/option[@value={season_value}]").click()
        time.sleep(2)
        d.find_element_by_xpath(f"//div[@data-type='results_only']").click()
        time.sleep(2)
        bs_season = bs(d.page_source, "html.parser")
        stages = [(opt.text.strip(), opt.get("value")) for opt in
                  bs_season.find("select", {"id": "33-303-filter-stage"}).find_all("option")]
        for k in range(3):
            # Go through all stages of season
            for j, (stage_text, stage_value) in enumerate(stages[1:]):
                print(stage_text)
                d.find_element_by_xpath(f"//select[@id='33-303-filter-stage']/option[@value={stage_value}]").click()
                time.sleep(2)
                bs_stage = bs(d.page_source, "html.parser")
                hrefs = get_hrefs(bs_stage, season_str, stage_text)
                pages = bs_stage.find("div", {"id": "schedule"}).find("ul", {"class": "mbt-v2-pagination"})

                # If there are more than one page, go through all pages
                if pages:
                    pages = pages.find_all("li")
                    for page in pages[1:-1]:
                        id_ = page.find("a").get("id")
                        d.find_element_by_xpath(f"//a[@id='{id_}']").click()
                        time.sleep(2)
                        bs_stage = bs(d.page_source, "html.parser")
                        hrefs.extend(get_hrefs(bs_stage, season_str, stage_text))
                if len(hrefs) > 0:
                    all_games.extend(hrefs)

    pd_all_games = pd.DataFrame(data=np.unique(np.array(all_games), axis=0), columns=["Season", "Stage", "Round", "Href"])
    pd_all_games.to_csv(f"{DATA_DIR}/game_hrefs.csv")


if __name__ == "__main__":
    BASE_URL = "https://www.kzs.si/"
    DATA_DIR = "../../../data/basketball/kzs"
    CHROME_DRIVER_PATH = "../other/chromedriver"

    create_dir()
    driver = selenium_driver(f"{BASE_URL}clanek/Tekmovanja/Liga-Nova-KBM/cid/66", CHROME_DRIVER_PATH)
    # get_all_games(driver)
    get_games_data(driver)
    driver.close()


# def get_games_hrefs(d):
#     games_hrefs = []
#     bs_main = bs(d.page_source, "html.parser")
#     seasons = [f"Saison {s_} / {s_ + 1}" for s_ in range(start_season, end_season + 1)]
#     for i, season in enumerate(seasons):
#         season_str = season.replace("Saison", "").replace(" ", "")
#         print(season_str)
#         d.find_element_by_xpath("(//div[@class=' css-1wy0on6'])[1]").click()
#         time.sleep(0.2)
#         d.find_element_by_xpath(f"//div[contains(text(),'{season}')]").click()
#         time.sleep(0.2)
#
#         for spieltag in range(1, 35):
#             d.find_element_by_xpath("//div[@data-testid='matchday-selector-delayed']//div[@class=' css-1wy0on6']").click()
#             time.sleep(0.2)
#             d.find_element_by_xpath(f"//div[contains(text(),'{spieltag}. Spieltag')]").click()
#             time.sleep(0.2)
#             d.find_element_by_xpath("//button[@data-testid='applyFilterButton']").click()
#             time.sleep(1)
#
#             if spieltag == 1 and i == 0:
#                 d.find_element_by_xpath("//button[@data-testid='games-toggle']").click()
#                 time.sleep(0.2)
#
#             f = bs(d.page_source, "html.parser")
#             hrefs = [a.get("href") for a in f.find_all("a", {"rel": "noreferrer"})][0::4]
#             print(len(hrefs), hrefs)
#
#     # df_href = pd.DataFrame(games_hrefs, columns=['season', 'part', 'href'])
#     # df_href.to_csv("../../data/vtb/hrefs.csv")
#     return games_hrefs
#
#
# driver = selenium_driver(f"{BASE_URL}saison/spielplaene_liga-pokalspiele/hauptrunde")
# get_games_hrefs(driver)
#
# hrefs = pd.read_csv("../../data/vtb/hrefs.csv")
# games_data = []
# for i, (index, season, season_part, game_h) in hrefs.iterrows():
#     print(game_h)
#     driver.get(game_h)
#     time.sleep(1)
#     driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
#     time.sleep(0.1)
#
#     rnd = None
#     bs_game_card = bs(driver.page_source, "html.parser")
#     q_scores = bs_game_card.find("div", {"class": "mbt-v2-game-quarter-scores"})
#     if not q_scores:
#         game_row = [season, season_part, rnd,
#                     date_string, ] ### end here I guess?
#         games_data.append(game_row)
#     quarters = [q.text.strip().split(" : ") for q in q_scores.find_all("span")]
#     h_quarters = [q_pair[0] for q_pair in quarters] + (8 - len(quarters)) * [None]
#     a_quarters = [q_pair[1] for q_pair in quarters] + (8 - len(quarters)) * [None]
#     h_code = bs_game_card.find("div", {"class": "mbt-v2-game-team-logo-a"}).find("a").get("team_id")
#     a_code = bs_game_card.find("div", {"class": "mbt-v2-game-team-logo-b"}).find("a").get("team_id")
#
#     driver.find_element_by_xpath(f"//div[@id='15-400-tab-1']").click()
#     time.sleep(1.2)
#
#     bs_box_score = bs(driver.page_source, "html.parser")
#     teams_div = bs_box_score.find("div", {"class": "mbt-v2-header"})
#     teams_div_list = teams_div.text.strip().split("\n")
#     h_name = teams_div_list[0].strip()
#     a_name = teams_div_list[4].strip()
#     h_score = int(teams_div_list[1].strip())
#     a_score = int(teams_div_list[3].strip())
#
#     match_info = [s.text.strip() for s in bs_box_score.find("div", {"class": "mbt-v2-game-main-information"}).find_all("span")]
#     date_split = match_info[0].split("/")
#     date_string = f"{date_split[1]}/{date_split[0]}/{date_split[2]}"
#     game_time = match_info[1]
#     venue = match_info[2]
#     attendance = None
#     if match_info[3].isnumeric():
#         attendance = int(match_info[3])
#
#     ref_text = bs_box_score.find(text=re.compile('Referees'))
#     ref1, ref2, ref3 = None, None, None
#     if ref_text:
#         refs = ref_text.parent.parent.text.strip().split("Referees:")[1]
#         ref1, ref2, ref3 = [ref.strip() for ref in refs.split(",")]
#
#     sums_h_td, sums_a_td = [g_.parent.parent for g_ in bs_box_score
#                             .find("table", {"id": "mbt-v2-game-boxscore-table"})
#                             .find_all(text=re.compile('Sums'))]
#     sums_h = [s.text.strip() for s in sums_h_td.find_all("td")]
#     sums_a = [s.text.strip() for s in sums_a_td.find_all("td")]
#     h_stats = sums_h[2].split("/") + sums_h[4].split("/") + sums_h[8].split("/") + sums_h[10:13] + \
#         [sums_h[13], sums_h[17], sums_h[16], sums_h[18], sums_h[19], sums_h[14], sums_h[15], sums_h[20]]
#     a_stats = sums_a[2].split("/") + sums_a[4].split("/") + sums_a[8].split("/") + sums_a[10:13] + \
#         [sums_a[13], sums_a[17], sums_a[16], sums_a[18], sums_a[19], sums_a[14], sums_a[15], sums_a[20]]
#
#     game_row = [
#         season, season_part, rnd,
#         date_string, game_time, venue,
#         attendance, ref1, ref2, ref3,
#         h_name, a_name, h_code, a_code,
#         h_score, a_score, *h_quarters,
#         *a_quarters, *h_stats, *a_stats
#     ]
#
#     print(game_row)
#     games_data.append(game_row)
# df_vtb = pd.DataFrame(data=games_data, columns=col_names)
# df_vtb.to_csv("../../data/vtb/vtb_games.csv", index=False)
#
# driver.close()
#
#
#
