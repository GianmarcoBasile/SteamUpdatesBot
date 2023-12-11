# pylint: skip-file
"""Module providing commands for the bot"""

import json
from database import initialize_db as db
from utils import get_game_list

redis_instance = db('localhost', 6379)
app_list = get_game_list()

async def start(update, context):
    redis_instance.set(update.message.from_user['username'], json.dumps({'games': {}}))
    await update.message.reply_text('Benvenuto su Steam News Bot!')

async def addGame(update, context):
    try:
        if context.args:
            game_name = ' '.join(context.args).lower()
            if game_name in app_list.values():
                games_list = json.loads(redis_instance.get(update.message.from_user['username']))['games']
                if not games_list:
                    games_json = {'games': {0: game_name}}
                    redis_instance.set(update.message.from_user['username'], json.dumps(games_json))
                    await update.message.reply_text('Games set to ' + game_name)
                else:
                    games = []
                    games_json = json.loads(redis_instance.get(update.message.from_user['username']))
                    if game_name not in games_json['games'].values():
                        games_json['games'].update({len(games_json['games']): game_name})
                        games = list(games_json['games'].values()) 
                        redis_instance.set(update.message.from_user['username'], json.dumps(games_json))
                        await update.message.reply_text('Games set to ' + str(games).replace('[', '').replace(']', '').replace("'", ''))
                    else:
                        await update.message.reply_text('Game already in your favorites')
            else:
                await update.message.reply_text('Game not found')
        else:
            await update.message.reply_text('La sintassi del comando prevede un argomento: /addgame <game_id>')
    except Exception as e:
        print(e)

async def deleteGame(update, context):    
    if context.args:
        game_name = ' '.join(context.args).lower()
        games_list = json.loads(redis_instance.get(update.message.from_user['username']))['games']
        if not games_list:
            await update.message.reply_text('La lista dei giochi preferiti è vuota')
        else:
            games_json = json.loads(redis_instance.get(update.message.from_user['username']))
            if game_name in games_json['games'].values():
                for key, value in games_json['games'].items():
                    if value == game_name:
                        games_json['games'].pop(key)
                        break                
                new_games_json = {'games':{}}
                for key, value in games_json['games'].items():
                    new_games_json['games'].update({len(new_games_json['games']): value})
                redis_instance.set(update.message.from_user['username'], json.dumps(new_games_json))
                await update.message.reply_text('Gioco ' + str(game_name)+ ' eliminato dalla lista ')
            else:
                await update.message.reply_text('Il gioco non è nella lista, impossibile eliminarlo')
    else:
        await update.message.reply_text('La sintassi del comando richiede un argomento: /deletegame <game_name>')
    
    
async def clearGamesList(update, context):
    redis_instance.set(update.message.from_user['username'], json.dumps({'games': {}}))
    await update.message.reply_text('Game list cleared')

# async def getNews(update, context):
#     global game_id
#     if context.args:
#         r = requests.get('http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + getGameIdByName(context.args[0]) + '&count=3&maxlength=300&format=json')
#         print(r.json())
#         await update.message.reply_text('News for game ' + context.args[0])
#     elif not context.args and game_id != '':
#         r = requests.get('http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + game_id + '&count=3&maxlength=300&format=json')
#         print(r.json())
#         await update.message.reply_text('News for game ' + game_id)
#     else:
#         await update.message.reply_text('La sintassi del comando prevede che tu abbia prima settato un gioco oppure che tu inserisca un argomento: /getnews <game_id>')

# async def getNews(context):
#     global game_id
#     print('gameid:', game_id)
#     r = requests.get('http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + game_id + '&count=3&maxlength=300&format=json')
#     print(r.json())
#     return r.json()

async def getFavoriteGames(update, context):
    games = list(json.loads(redis_instance.get(update.message.from_user['username']))['games'].values())
    print(games)
    await update.message.reply_text('Favorite Games: ' + str(games).replace('[', '').replace(']', '').replace("'", ''))
