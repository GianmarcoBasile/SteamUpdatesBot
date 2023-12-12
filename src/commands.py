# pylint: skip-file
"""Module providing commands for the bot"""

import json
import requests
from database import initialize_db as db
from utils import get_game_list, get_game_id_by_name

mongo_instance = db('mongodb://localhost', 27017)
app_list = get_game_list()
syntax_error = 'The correct syntax for this command is: '

async def start(update, context):
    sender = update.message.from_user['username']
    if not mongo_instance['USERS'][sender].find_one({'chat_id': update.message.chat_id}):
        mongo_instance['USERS'][sender].insert_one({'chat_id': update.message.chat_id})
        mongo_instance['GAMES']['games'].insert_one({'user': sender, 'games': {}})
    await update.message.reply_text('Welcome to Steam News Bot!')

async def addGame(update, context):
    try:
        if context.args:
            game_name = ' '.join(context.args).lower()
            if game_name in app_list.values():
                games_record = mongo_instance['GAMES']['games'].find_one({'user': update.message.from_user['username']})
                print(games_record)
                if game_name not in games_record['games'].values():
                    if(games_record['games'] == {}):
                        games_record['games'] = {'0': game_name}
                    else:
                        games_record['games'].update({str(int(max(games_record['games']))+1): game_name})
                    print(games_record)
                    mongo_instance['GAMES']['games'].update_one({'user': update.message.from_user['username']}, {'$set': games_record})
                    await update.message.reply_text('Game ' + str(game_name) + ' added to the list')
                else:
                    await update.message.reply_text('The game is already in the list')
            else:
                await update.message.reply_text('The game is not a steam game')
        else:
            await update.message.reply_text(syntax_error + '/addgame <game_name>')
    except Exception as e:
        print(e)

async def deleteGame(update, context):    
    if context.args:
        game_name = ' '.join(context.args).lower()
        games_record = mongo_instance['GAMES']['games'].find_one({'user': update.message.from_user['username']})
        if game_name in games_record['games'].values():
            games_record['games'].pop(str(list(games_record['games'].values()).index(game_name)))
            mongo_instance['GAMES']['games'].update_one({'user': update.message.from_user['username']}, {'$set': games_record})
            await update.message.reply_text('Game ' + str(game_name) + ' deleted from the list')
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
