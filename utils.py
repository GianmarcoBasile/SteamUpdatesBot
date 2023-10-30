import requests

def getGamesList():
    r = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v0002/')
    app_list_tmp = r.json()['applist']['apps']
    app_list = {}
    for x in app_list_tmp:
        app_list.update({x['appid']: x['name'].lower()})
    return app_list

def getGameIdByName(name):
    for x in app_list:
        if app_list[x] == name:
            return x
    return None

