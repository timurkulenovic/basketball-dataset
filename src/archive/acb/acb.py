from bs4 import BeautifulSoup as bs
import requests
import re
from scrape.basketball.helpers import col_names
import pandas as pd
import os

BASE_URL = "https://www.acb.com"
games_data = []


if not os.path.exists('../../data/acb'):
    os.makedirs('../../data/acb')


for season_value in range(2021, 2022):
    season = f"{season_value}/{season_value + 1}"
    season_part = None
    rnd = 1
    while True:
        req_rnd = requests.get(f'{BASE_URL}/resultados-clasificacion/ver/temporada_id/{season_value}/competicion_id/1/jornada_numero/{rnd}')
        bs_round = bs(req_rnd.text, "html.parser")
        game_list_bs = bs_round.find("div", {"id": "listado_partidos"})
        g_hrefs = [g.find("div", {"class": "resultado"}).find("a").get("href") for g in game_list_bs.find_all("div", {"class": "info"})
                   if g.find("div", {"class": "resultado"})]
        if len(g_hrefs) == 0:
            break
        for href in g_hrefs:
            req_game = requests.get(f'{BASE_URL}{href}')
            bs_game = bs(req_game.text, "html.parser")

            # Team names
            h_name = bs_game.find_all("h4", {"class": "clase_mostrar_block960"})[0].text.strip()
            a_name = bs_game.find_all("h4", {"class": "clase_mostrar_block960"})[1].text.strip()

            # Date, time, venue, attendance
            info = bs_game.find("div", {"class": "datos_fecha"})
            if info is None:
                continue
            _, date, time, venue, att = info.text.split(" | ")
            venue = venue[:int(len(venue)/2)]
            date_list = date.split("/")
            date_string = f"{date_list[2]}/{date_list[1]}/{date_list[0]}"
            attendance = att.replace("Público: ", "").replace(".", "").strip()

            # Scores
            scores = bs_game.find("div", {"class": "info"}).find_all("div", {"class": "resultado"})
            h_score, a_score = [s.text for s in scores]

            # Scores by quarters
            _, q_box_h, q_box_a = bs_game.find("div", {"class": "contenedora_tabla"}).find_all("tr")
            h_quarters = [s.text for s in q_box_h.find_all("td")[2:-1]]
            a_quarters = [s.text for s in q_box_a.find_all("td")[2:-1]]

            # Add None for 4 overtimes
            h_quarters = h_quarters + ((8 - len(h_quarters)) * [None])
            a_quarters = a_quarters + ((8 - len(a_quarters)) * [None])

            # Referees
            refs = bs_game.find("div", {"class": "datos_arbitros"}).text.replace("Árb: ", "").split(", ")
            ref1, ref2, ref3 = None, None, None
            if len(refs) == 2:
                ref1, ref2 = refs
            elif len(refs) == 3:
                ref1, ref2, ref3 = refs

            # Team codes
            codes = bs_game.find("div", {"class": "contenedora_info_principal"}).find_all("div", {"class": "logo_equipo"})
            h_code = codes[0].find("a").get("href").split("/")[4]
            a_code = codes[1].find("a").get("href").split("/")[4]

            # Box score data
            box_score_h, box_score_a = bs_game.find_all("section", "partido")
            h_td = [td.text for td in box_score_h.find("tr", {"class": "totales"}).find_all("td")]
            h_stats = h_td[4].split("/") + h_td[6].split("/") + h_td[8].split("/") + h_td[11].split("+") + [h_td[10]] +\
                      h_td[12:15] + h_td[16:18] + h_td[19:21] + [h_td[22]]
            a_td = [td.text for td in box_score_a.find("tr", {"class": "totales"}).find_all("td")]
            a_stats = a_td[4].split("/") + a_td[6].split("/") + a_td[8].split("/") + a_td[11].split("+") + [a_td[10]] +\
                      a_td[12:15] + a_td[16:18] + a_td[19:21] + [a_td[22]]

            # Gather all the data
            game_row = [
                season, season_part, rnd,
                date_string, time, venue,
                attendance, ref1, ref2, ref3,
                h_name, a_name, h_code, a_code,
                h_score, a_score, *h_quarters,
                *a_quarters, *h_stats, *a_stats
            ]
            print(game_row)
            games_data.append(game_row)
        rnd += 1

    df_aba = pd.DataFrame(data=games_data, columns=col_names)
    df_aba.to_csv("../../data/acb/acb_games.csv")
