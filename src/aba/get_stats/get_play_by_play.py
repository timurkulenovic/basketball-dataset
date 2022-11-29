import re
import numpy as np
import pandas as pd


def get_row_data(td):
    a = td.find("a")
    text = td.text
    player_number = pd.NA
    player_id = pd.NA
    player_name = pd.NA
    play = pd.NA
    play_note = pd.NA

    missing_data = False
    if a is None:
        play_note = text[text.find("(") + 1:text.find(")")]
        missing_data = True
    else:
        player_id = a.get("href").split("/")[2]
        player_name = a.text.strip()
        text = text.replace(player_name, "")

        if "(" in text and ")" in text:
            play_note = text[text.find("(") + 1:text.find(")")]
            text = text.replace(f"({play_note})", "")

        numbers = re.findall(r'\d+', text)
        player_number = int(numbers[0]) if len(numbers) > 0 else pd.NA
        play = text.replace(str(player_number), "").replace(".", "").strip()

    return player_number, player_id, player_name, play, play_note, missing_data


def extract_play_by_play(bs_play_by_play, part_id, h_img_id, a_img_id):
    bs_q_part = bs_play_by_play.find("div", {"id": part_id})
    if bs_q_part is None:
        return []
    bs_q_rows = bs_q_part.find("table", {"class": "match_table_play_by_play"}).find("tbody").find_all("tr")

    play_by_play_part = []

    for q_row in bs_q_rows:
        home_td, middle_td, away_td = q_row.find_all("td")
        middle_text = middle_td.text

        team = pd.NA
        clock_minutes = pd.NA
        clock_seconds = pd.NA
        player_number = pd.NA
        player_id = pd.NA
        player_name = pd.NA
        play = pd.NA
        play_note = pd.NA
        missing_data = pd.NA

        # Check if play is timeout
        if "Timeout" in middle_td.text:
            play = "timeout"
            img_id = middle_td.find("img").get("src").split("/")[-1].split(".")[0].strip()
            if img_id == h_img_id:
                team = "H"
            elif img_id == a_img_id:
                team = "A"
            middle_text = middle_text.replace("Timeout", "")

        if "timeout - officials" in middle_text:
            play = "timeout - officials"
            middle_text = middle_text.replace(play, "")

        # Extract score
        h_score, a_score = pd.NA, pd.NA
        score_span = middle_td.find("span", {"class": "td-rezultat"})
        if score_span:
            middle_text = middle_text.replace(score_span.text, "")
            h_score, a_score = [int(score) for score in score_span.text.split(" : ")]

        # Extract clock
        if ":" in middle_text:
            clock_minutes, clock_seconds = [int(unit) for unit in middle_text.strip().split(":")]
        else:
            play = middle_text.strip()

        # Extract player and play
        if home_td.text != "":
            team = "H"
            player_number, player_id, player_name, play, play_note, missing_data = get_row_data(home_td)
        elif away_td.text != "":
            team = "A"
            player_number, player_id, player_name, play, play_note, missing_data = get_row_data(away_td)

        play_by_play_part.append([clock_minutes, clock_seconds, team,
                                  h_score, a_score, player_number,
                                  player_id, player_name, play,
                                  play_note, missing_data])

    return np.flip(np.array(play_by_play_part), 0)


def get_play_by_play(bs_object, game_data):
    bs_play_by_play = bs_object.find("div", {"class": "match_tab_content_container_play_by_play"})
    if bs_play_by_play.text == "No play by play data for this match.":
        return []
    bs_teams_img = bs_object.find("div", {"id": "match_clubs_and_results_info_table"}).find_all("img")
    h_img_id, a_img_id = [img.get("src").split("/")[-1].split(".")[0].strip() for img in bs_teams_img]

    play_by_play_data = []
    for part, part_id in [(1, "q1"), (2, "q2"), (3, "q3"), (4, "q4"), ("OT", "q5")]:
        play_by_play_part = extract_play_by_play(bs_play_by_play, part_id, h_img_id, a_img_id)
        if len(play_by_play_part) > 0:
            play_by_play_part = np.insert(play_by_play_part, 0, part, axis=1)
            play_by_play_data.append(play_by_play_part)

    if len(play_by_play_data) == 0:
        return []
    
    play_by_play_data = np.concatenate(play_by_play_data, axis=0)
    play_by_play_data = np.insert(play_by_play_data, 0, game_data["ID"], axis=1)
    play_by_play_data = np.insert(play_by_play_data, 0, game_data["Season"], axis=1)
    return play_by_play_data

