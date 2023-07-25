from bs4 import BeautifulSoup as bs
import re
import numpy as np
import pandas as pd


def get_team_ids(bs_object):
    title = bs_object.find("h1", {"class": "main_title"})
    h_id, a_id = title.text.strip().split(" - ")
    return h_id, a_id


def get_venue_and_attendance(bs_object):
    date_venue = bs_object.find("div", {"class": "dateAndVenue_container"})
    date_venue_str = str(date_venue).split("<br/>")
    date_venue_list = [bs(el, "html.parser").text.strip() for el in date_venue_str]

    # Logic for cases when venue or
    # attendance information is missing
    if len(date_venue_list) == 3:
        attendance = int(date_venue_list[1])
        venue = date_venue_list[2].split(":")[1].strip()
    elif len(date_venue_list) == 2:
        if date_venue.find("i"):
            attendance = int(date_venue_list[1])
            venue = pd.NA
        else:
            attendance = pd.NA
            venue = date_venue_list[1].split(":")[1].strip()
    else:
        venue = pd.NA
        attendance = pd.NA
    return venue, attendance


def get_scores_by_quarters(bs_object):
    quarters_table = bs_object.find("table", {"id": "match_cetrtine_rezultat"})
    quarters_scores = [q_sc.text.split(":") for q_sc in quarters_table.find_all("tr")[1].find_all("td")]
    h_quarters = [s[0].strip() for s in quarters_scores]
    a_quarters = [s[1].strip() for s in quarters_scores]

    # Add None for 4 overtimes
    h_quarters = h_quarters + ((8 - len(h_quarters)) * [pd.NA])
    a_quarters = a_quarters + ((8 - len(a_quarters)) * [pd.NA])

    return h_quarters, a_quarters


def get_referees(bs_object):
    ref_div = bs_object.find(text=re.compile('Referees:'))
    ref1, ref2, ref3 = pd.NA, pd.NA, pd.NA
    if ref_div:
        refs = ref_div.parent.parent.text.split("Referees:")[1].strip().split(", ")
        if len(refs) == 2:
            ref1, ref2 = refs
        elif len(refs) == 3:
            ref1, ref2, ref3 = refs
    return ref1, ref2, ref3


def get_main_info(bs_object, game_data, BASE_URL):
    h_id, a_id = get_team_ids(bs_object)
    venue, attendance = get_venue_and_attendance(bs_object)
    h_quarters, a_quarters = get_scores_by_quarters(bs_object)
    ref1, ref2, ref3 = get_referees(bs_object)

    main_info = [game_data["Season"], game_data["ID"], game_data["Stage"], game_data["Round"],
                 game_data["Date"], game_data["Time"], venue, attendance,
                 ref1, ref2, ref3, game_data["H_Team"], game_data["A_Team"], h_id, a_id,
                 game_data["H_Score"], game_data["A_Score"], *h_quarters, *a_quarters]

    return np.array([main_info])
