# pylint: skip-file
"""Module providing commands for the bot"""

import json
import requests
from database import initialize_db as db
from utils import get_game_list, get_game_id_by_name

mongo_instance = db('mongodb://0.0.0.0', 27017)
app_list = get_game_list()
syntax_error = 'The correct syntax for this command is: '

async def start(update, context):
    mongo_instance.set(update.message.from_user['username'], json.dumps({'games': {}}))
    await update.message.reply_text('Welcome to Steam News Bot!')

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
            await update.message.reply_text(required_argument + '/addgame <game_name>')
    except Exception as e:
        print(e)

async def deleteGame(update, context):    
    if context.args:
        game_name = ' '.join(context.args).lower()
        games_list = json.loads(redis_instance.get(update.message.from_user['username']))['games']
        if not games_list:
            await update.message.reply_text('The favourite game list is empty')
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
                await update.message.reply_text('Game ' + str(game_name)+ ' removed from the list')
            else:
                await update.message.reply_text('The game is not in the list')
    else:
        await update.message.reply_text(required_argument + '/deletegame <game_name>')
    
    
async def clearGamesList(update, context):
    redis_instance.set(update.message.from_user['username'], json.dumps({'games': {}}))
    await update.message.reply_text('Game list cleared')

async def getNews(update, context):
    if not context.args:
        games = json.loads(redis_instance.get(update.message.from_user['username']))['games']
        games_news_record = json.loads(redis_instance.get(update.message.from_user['username']))['games']
        for game in games.values():
            r = requests.get('http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + str(get_game_id_by_name(game)) + '&count=3&maxlength=300&format=json')
            print(r.json())

    else:
        await update.message.reply_text(syntax_error + '/getnews')

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
