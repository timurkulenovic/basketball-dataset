import numpy as np
from bs4 import BeautifulSoup


def get_play_by_play(bs_object, game_data, BASE_URL):
    table = bs_object.find("table", {"class": "mbt-v2-table mbt-v2-game-play-by-play-table"})
    if not table:
        return []
    rows = table.find("tbody").find_all("tr")
    part = 1
    play_by_play = []
    for row in rows:
        td = row.find_all("td")
        if len(td) > 1:
            light_text = td[3].find("span", {"class": "mbt-v2-text-light"})
            if light_text:
                team = light_text.text.strip()
            else:
                team = td[2].find("img").get("alt")
            clock, res = td[0].text.strip(), td[1].text.strip()
            actions = [BeautifulSoup(action_i, 'html.parser') for action_i in str(td[3]).split('<br/>')]
            for action in actions:
                player_ids = [a.get("player_id") for a in action.find_all("a")]
                action = action.text.strip().replace("/a", "")
                action = action.split("\n")
                if len(action) == 3:
                    action = action[2]
                else:
                    action = action[0]
                player_number, player_name, player_id = None, None, None
                if " je " in action:
                    player, action = action.split(" je ")
                    player_number, player_name = player.split(")")
                    player_name = player_name.strip()
                    player_number = player_number.replace("(", "").strip()
                    player_id = player_ids[0]
                acted_on = None
                if "na (" in action:
                    action, acted_on = action.split(" na ")
                    acted_on = acted_on.split(") ")[1]

                h_points, a_points = None, None
                if len(res) > 0:
                    h_points, a_points = [int(p) for p in res.split(":")]

                minutes, sec = [int(t) for t in clock.split(":")]
                minutes_quarter = int(minutes) % 10

                play_note = None
                if acted_on:
                    play_note = "Acted on " + acted_on

                new_row = [game_data["Season"], game_data["ID"], part, minutes_quarter, sec,
                           team, h_points, a_points, player_number, player_id, player_name, action, play_note, False]

                play_by_play.append(new_row)
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
            new_row = [game_data["Season"], game_data["ID"], part] + 8 * [None] + [action] + 2 * [None]
            play_by_play.append(new_row)

    return np.array(play_by_play)
