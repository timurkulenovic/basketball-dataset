import numpy as np


def get_comments(bs_object, game_data, BASE_URL):
    comments_data = []
    comments_bs = bs_object.find("div", {"id": "Comments"})
    persons = [strong.text for strong in comments_bs.find_all("strong")]
    if len(persons) == 0:
        persons = [strong.text for strong in comments_bs.find_all("b")]
    comments = [comment.text for comment in comments_bs.find_all("em")]

    if all([True if "trener" not in person else False for person in persons]):
        persons = [f"{persons[i]}, trener {persons[i + 1]}" for i in range(0, len(persons), 2)]

    # Sometimes comments are not inside "em"
    if len(comments) == 0:
        comments_text = comments_bs.text
        for person in persons:
            comments_text = comments_text.replace(person, "")
        comments_text = comments_text.replace("Comments", "").replace("\r", "")
        comments = [sentence for sentence in comments_text.split("\n") if len(sentence) > 5]

    for person, comment in zip(persons, comments):
        name, role = person.split("trener")
        name = name.replace(",", "").strip()
        role = f'trener {role.replace(":", "").strip()}'
        comment_content = comment.replace('„', '').replace('"', '').replace('“', '').replace('”', '')
        comments_data.append([name, role, comment_content])

    comments_data = np.array(comments_data)
    comments_data = np.insert(comments_data, 0, game_data["ID"], axis=1)
    comments_data = np.insert(comments_data, 0, game_data["Season"], axis=1)

    return np.array(comments_data)
