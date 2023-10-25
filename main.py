from telegram.ext import *
from bot import Bot
import requests
import re
import asyncio

game_id = ''

# http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=440&count=3&maxlength=300&format=json
async def setGame(update, context):
    if context.args:
        await update.message.reply_text('Game set to ' + context.args[0])
    else:
        await update.message.reply_text('La sintassi del comando prevede un argomento: /setgame <game_id>')

async def getNews(update, context):
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
def main():
    bot_instance = Bot()
    application = Application.builder().token(bot_instance.getToken()).build()

    # Commands
    application.add_handler(CommandHandler('setgame', setGame))
    application.add_handler(CommandHandler('getnews', getNews))

    # Run bot
    application.run_polling(1.0)

if __name__ == '__main__':
    main()