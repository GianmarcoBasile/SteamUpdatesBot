"""Module providing utility functions for the code."""

import json
import requests


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
