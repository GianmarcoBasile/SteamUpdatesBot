"""Module providing utility functions for the code."""

import requests

def get_game_list():
    """Function that requests the list of games from the Steam API."""
    r = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v0002/', timeout=10)
    app_list_tmp = r.json()['applist']['apps']
    app_list = {}
    for x in app_list_tmp:
        app_list.update({x['appid']: x['name'].lower()})
    return app_list

def get_game_id_by_name(name):
    """Function that get the game id from the game name."""
    app_list = get_game_list()
    for x in app_list.items():
        if app_list[x] == name:
            return x
    return None
