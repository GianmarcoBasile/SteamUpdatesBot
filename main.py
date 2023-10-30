from telegram.ext import *
import os
from bot import Bot
import requests
import re
import asyncio
import time
import redis
import json
from dotenv import load_dotenv


load_dotenv()
print('os.environ:', os.environ['API_KEY'])
bot_instance = Bot(os.environ['API_KEY'])
redis_instance = redis.Redis(host='localhost', port=6379, decode_responses=True)
r = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v0002/')
app_list_tmp = r.json()['applist']['apps']
app_list = {}
for x in app_list_tmp:
    app_list.update({x['appid']: x['name']})

def getGameIdByName(name):
    for x in app_list:
        if app_list[x] == name:
            return x
    return None

# http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=440&count=3&maxlength=300&format=json
async def setGame(update, context):
    # TEST: redis_instance.set('gianmarco', json.dumps({'games': '1234'}))
    try:
        if context.args:
            user_record = redis_instance.get(update.message.from_user['username'])
            if not user_record:
                games = {'games_id': {0: context.args[0]}}
                redis_instance.set(update.message.from_user['username'], json.dumps(games))
            else:                
                games = json.loads(redis_instance.get(update.message.from_user['username']))
                games['games_id'].update({len(games['games_id']): context.args[0]})
                redis_instance.set(update.message.from_user['username'], json.dumps(games))
            await update.message.reply_text('Game set to ' + games['games_id'])
        else:
            await update.message.reply_text('La sintassi del comando prevede un argomento: /setgame <game_id>')
    except Exception as e:
        print(e)

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

    
async def getGame(update, context):
    games_id = redis_instance.hgetall(update.message.from_user)['games_id']
    print('games_id:', game_id)
    await update.message.reply_text('game_id -> ' + game_id)

def main():
    # Commands
    bot_instance.application.add_handler(CommandHandler('setgame', setGame))
    # application.add_handler(CommandHandler('getnews', getNews))
    bot_instance.application.add_handler(CommandHandler('getgame', getGame))
    # application.job_queue.run_repeating(getNews, interval=10, first=0)

    # Run bot
    bot_instance.application.run_polling(1.0)


if __name__ == '__main__':
    main()