import pandas as pd


def get_score_evolution(bs_object, game_data, BASE_URL):
    development_graph = bs_object.find("div", {"id": "33-400-development-graph"})
    if not development_graph:
        return []
    script = development_graph.find("script")
    if not script:
        return []
    data = script.text.split("\n")[3].split("data = ")[1].replace(";", "")
    df = pd.read_json(data)
    df.insert(0, "SEASON", game_data["Season"])
    df.insert(1, "GAME_ID", game_data["ID"])
    return df
