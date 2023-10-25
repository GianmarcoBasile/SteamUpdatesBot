from telegram.ext import *
from bot import Bot
import requests
import re
import asyncio
import time

bot_instance = Bot()
application = Application.builder().token(bot_instance.getToken()).build()
game_id = ''

# http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=440&count=3&maxlength=300&format=json
async def setGame(update, context):
    if context.args:
        global game_id
        game_id = context.args[0]
        application.job_queue.run_repeating(getNews, interval=10, first=0)
        await update.message.reply_text('Game set to ' + game_id)
    else:
        await update.message.reply_text('La sintassi del comando prevede un argomento: /setgame <game_id>')

async def getNews(update, context):
    global game_id
    if context.args:
        r = requests.get('http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + context.args[0] + '&count=3&maxlength=300&format=json')
        print(r.json())
        await update.message.reply_text('News for game ' + context.args[0])
    elif not context.args and game_id != '':
        r = requests.get('http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + game_id + '&count=3&maxlength=300&format=json')
        print(r.json())
        await update.message.reply_text('News for game ' + game_id)
    else:
        await update.message.reply_text('La sintassi del comando prevede che tu abbia prima settato un gioco oppure che tu inserisca un argomento: /getnews <game_id>')

async def getNews(context):
    global game_id
    print('gameid:', game_id)
    r = requests.get('http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + game_id + '&count=3&maxlength=300&format=json')
    print(r.json())
    return r.json()

    
async def getGame(update, context):
    global game_id
    print('gameid:', game_id)
    await update.message.reply_text('game_id -> ' + game_id)

def main():
    # Commands
    application.add_handler(CommandHandler('setgame', setGame))
    application.add_handler(CommandHandler('getnews', getNews))
    application.add_handler(CommandHandler('getgame', getGame))
    application.job_queue.run_repeating(getNews, interval=10, first=0)

    # Run bot
    application.run_polling(1.0)

if __name__ == '__main__':
    main()