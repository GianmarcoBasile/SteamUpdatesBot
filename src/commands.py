# pylint: skip-file
"""Module providing commands for the bot"""

import json
import requests
from telegram import Update
from database import initialize_db as db
from utils import (
    find_users,
    get_game_list,
    get_game_id_by_name,
    check_similarities,
    get_games_record,
    jsonify,
    update_games_record,
)
from news_parser import parser
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

mongo_instance = db("mongodb://localhost", 27017)
app_list = get_game_list()
syntax_error = "The correct syntax for this command is: "


async def start(update: Update, context: CallbackContext) -> None:
    sender = update.message.from_user["username"]
    if not mongo_instance["USERS"]["users"].find_one(
        {"chat_id": update.message.chat_id}
    ):
        mongo_instance["USERS"]["users"].insert_one(
            {"chat_id": update.message.chat_id, "user": sender, "games": {}}
        )
    await update.message.reply_text("Welcome to Steam News Bot!")


async def addGame(update: Update, context: CallbackContext) -> None:
    games_record = {}
    try:
        if context.args:
            game_name = " ".join(context.args).lower()
            if game_name in app_list.values():
                try:
                    games_record = get_games_record(
                        update.message.from_user["username"]
                    )
                except Exception as e:
                    print(e)
                if game_name not in games_record["games"].values():
                    if games_record["games"] == {}:
                        games_record["games"] = {"0": game_name}
                    else:
                        games_record["games"].update(
                            {str(int(max(games_record["games"])) + 1): game_name}
                        )
                    update_games_record(
                        update.message.from_user["username"], games_record
                    )
                    await update.message.reply_text(
                        "Game " + str(game_name) + " added to the list"
                    )
                else:
                    await update.message.reply_text("The game is already in the list")
            else:
                suggestions = check_similarities(game_name)
                if len(suggestions) > 0:
                    await update.message.reply_text(
                        "Game not found. Maybe you meant: " + suggestions
                    )
                else:
                    await update.message.reply_text("The game is not a steam game")
        else:
            await update.message.reply_text(syntax_error + "/addgame <game_name>")
    except Exception as e:
        print(e)


async def deleteGame(update: Update, context: CallbackContext) -> None:
    if context.args:
        game_name = " ".join(context.args).lower()
        try:
            games_record = get_games_record(update.message.from_user["username"])
        except Exception as e:
            print(e)
        if game_name in games_record["games"].values():
            games_record["games"].pop(
                str(list(games_record["games"].values()).index(game_name))
            )
            update_games_record(update.message.from_user["username"], games_record)
            await update.message.reply_text(
                "Game " + str(game_name) + " deleted from the list"
            )
        else:
            await update.message.reply_text("The game is not in the list")
    else:
        await update.message.reply_text(syntax_error + "/deletegame <game_name>")


async def clearGamesList(update: Update, context: CallbackContext) -> None:
    if not context.args:
        try:
            games_record = get_games_record(update.message.from_user["username"])
        except Exception as e:
            print(e)
        games_record["games"] = {}
        update_games_record(update.message.from_user["username"], games_record)
        await update.message.reply_text("Games list cleared")
    else:
        await update.message.reply_text(syntax_error + "/cleargameslist")


async def getNews(update: Update, context: CallbackContext) -> None:
    if not context.args:
        try:
            games = get_games_record(update.message.from_user["username"])
            for game in games["games"].values():
                r = requests.get(
                    "http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid="
                    + str(get_game_id_by_name(game))
                    + "&count=5&maxlength=50000&format=json"
                )
                news_list = jsonify(r)["appnews"]["newsitems"]
                for news in news_list:
                    news_message = parser(news)
                    await update.message.reply_text(
                        news_message, parse_mode=ParseMode.HTML
                    )
        except Exception as e:
            print(e)
    else:
        await update.message.reply_text(syntax_error + "/getnews")


async def getNewsAuto(context: CallbackContext) -> None:
    users = find_users()
    for user in users:
        for game in user["games"].values():
            r = requests.get(
                "http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid="
                + str(get_game_id_by_name(game))
                + "&count=1&maxlength=50000&format=json"
            )
            news_list = r.json()["appnews"]["newsitems"]
            for news in news_list:
                news_message = parser(news)
                await context.bot.send_message(
                    user["chat_id"], news_message, parse_mode=ParseMode.HTML
                )


async def getFavoriteGames(update: Update, context: CallbackContext) -> None:
    if not context.args:
        try:
            games_record = get_games_record(update.message.from_user["username"])
        except Exception as e:
            print(e)
        games = list(games_record["games"].values())
        await update.message.reply_text(
            "Favorite Games: "
            + str(games).replace("[", "").replace("]", "").replace("'", "")
        )
    else:
        await update.message.reply_text(syntax_error + "/favoritegames")


async def saleOnGames(update: Update, context: CallbackContext) -> None:
    if not context.args:
        games_record = get_games_record(update.message.from_user["username"])
        for game in games_record["games"].values():
            game_id = str(get_game_id_by_name(game))
            r = requests.get(
                "https://store.steampowered.com/api/appdetails/?appids="
                + game_id
                + "&currency=EUR"
            )
            req = jsonify(r)[game_id]
            if req["success"]:
                curr_game = req["data"]
                if curr_game["is_free"]:
                    await update.message.reply_text("The game " + game + " is free")
                elif (
                    curr_game["price_overview"]["initial"]
                    == curr_game["price_overview"]["final"]
                ):
                    await update.message.reply_text(
                        "The game "
                        + game
                        + " is not on sale. It costs "
                        + curr_game["price_overview"]["final_formatted"]
                    )
                else:
                    await update.message.reply_text(
                        "The game "
                        + game
                        + " is on sale for "
                        + curr_game["price_overview"]["final_formatted"]
                        + " instead of "
                        + curr_game["price_overview"]["initial_formatted"]
                    )
    else:
        await update.message.reply_text(syntax_error + "/checksales")


async def saleOnGamesAuto(context: CallbackContext) -> None:
    users = find_users()
    for user in users:
        for game in user["games"].values():
            game_id = str(get_game_id_by_name(game))
            r = requests.get(
                "https://store.steampowered.com/api/appdetails/?appids="
                + game_id
                + "&currency=EUR"
            )
            req = jsonify(r)[game_id]
            if req["success"]:
                curr_game = req["data"]
                if curr_game["is_free"]:
                    await context.bot.send_message(
                        user["chat_id"], "The game " + game + " is free"
                    )
                elif (
                    curr_game["price_overview"]["initial"]
                    == curr_game["price_overview"]["final"]
                ):
                    await context.bot.send_message(
                        user["chat_id"], "The game " + game + " is not on sale"
                    )
                else:
                    await context.bot.send_message(
                        user["chat_id"],
                        "The game "
                        + game
                        + " is on sale for "
                        + curr_game["price_overview"]["final_formatted"],
                    )
