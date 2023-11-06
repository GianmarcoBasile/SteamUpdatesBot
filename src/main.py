"""Main module of the BOT"""

import os
from telegram.ext import CommandHandler
from dotenv import load_dotenv
from bot import Bot
from commands import start, setGame, addGame, getFavoriteGames, clearGamesList

load_dotenv()
API_KEY = os.environ['API_KEY']
bot_instance = Bot(API_KEY)

# http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=440&count=3&maxlength=300&format=json

def main():
    """Main function which runs the bot and adds the handlers"""
    # Commands
    bot_instance.application.add_handler(CommandHandler('start', start))
    bot_instance.application.add_handler(CommandHandler('setgame', setGame))
    # application.add_handler(CommandHandler('getnews', getNews))
    bot_instance.application.add_handler(CommandHandler('addgame', addGame))
    bot_instance.application.add_handler(CommandHandler('favoritegames', getFavoriteGames))
    bot_instance.application.add_handler(CommandHandler('cleargameslist', clearGamesList))
    # application.job_queue.run_repeating(getNews, interval=10, first=0)
    # Run bot
    bot_instance.application.run_polling(1.0)

if __name__ == '__main__':
    main()
