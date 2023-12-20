"""Module providing utility functions for the code."""

import json
import requests

max_suggestions = 5

def get_game_list():
    """Function that requests the list of games from the Steam API."""
    r = requests.get(
        "https://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json"
    )
    app_list_tmp = r.json()["applist"]["apps"]
    app_list = {}
    for x in app_list_tmp:
        app_list.update({x["appid"]: x["name"].lower()})
    return app_list


app_list = get_game_list()


def get_game_id_by_name(name):
    """Function that get the game id from the game name."""
    for x in app_list.items():
        if x[1] == name:
            return x[0]
    return None


def get_game_name_by_id(game_id):
    """Function that get the game name from the id."""
    return app_list[game_id]

def check_similarities(wrong_name):
    first_part = wrong_name.split()[0]
    suggestions = []
    sugg_str = ""
    for game_id in app_list:
        game = get_game_name_by_id(game_id)
        if game.startswith(first_part):
            suggestions.append(game)
        if len(suggestions) > max_suggestions:
            break
    for elem in suggestions:
        sugg_str = sugg_str + elem + " , "
    if len(sugg_str) > 0:
        sugg_str= sugg_str[:-2]
    return sugg_str