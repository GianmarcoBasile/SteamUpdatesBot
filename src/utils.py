"""Module providing utility functions for the code."""

import requests
from database import initialize_db as db

MAX_SUGGESTION = 5


def get_game_list() -> dict:
    """Function that requests the list of games from the Steam API."""
    r = requests.get(
        "https://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json",
        timeout=60,
    )
    app_list_tmp = r.json()["applist"]["apps"]
    _app_list = {}
    for x in app_list_tmp:
        _app_list.update({x["appid"]: x["name"].lower()})
    return _app_list


app_list = get_game_list()


def get_game_id_by_name(name: str) -> int:
    """Function that get the game id from the game name."""
    for x in app_list.items():
        if x[1] == name:
            return x[0]
    return None


def get_game_name_by_id(game_id: int) -> str:
    """Function that get the game name from the id."""
    return app_list[game_id]


def check_similarities(wrong_name: str) -> str:
    """Function that checks if there are similar games in the database."""
    first_part = wrong_name.split()[0]
    if len(wrong_name.split()) > 1:
        second_part = wrong_name.split()[1]
    else:
        second_part = ""
    suggestions = []
    sugg_str = ""
    for game_id in app_list:
        game = get_game_name_by_id(game_id)
        if game.startswith(first_part) and second_part in game:
            if game not in suggestions:
                suggestions.append(game)
    suggestions.sort()
    for elem in suggestions[: min(MAX_SUGGESTION, len(suggestions))]:
        sugg_str = sugg_str + elem + ", "
    if len(sugg_str) > 0:
        sugg_str = sugg_str[:-2]
    return sugg_str


def get_games_record(username: str) -> dict:
    """Function that get the games record from the database."""
    mongo_instance = db("mongodb://localhost", 27017)
    return mongo_instance["USERS"]["users"].find_one({"user": username})


def find_users() -> dict:
    """Function that get the games record from the database."""
    mongo_instance = db("mongodb://localhost", 27017)
    return mongo_instance["USERS"]["users"].find()


def update_games_record(username: str, games_record: dict) -> None:
    """Function that updates the games record in the database."""
    mongo_instance = db("mongodb://localhost", 27017)
    mongo_instance["USERS"]["users"].update_one(
        {"user": username}, {"$set": games_record}
    )


def jsonify(data: requests.Response) -> dict:
    """Function that converts a dictionary to a json string."""
    return data.json()
