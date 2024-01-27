"""Module providing parsing for the game news"""

from datetime import datetime
from utils import get_game_name_by_id


def parser(news):
    """Function that parses the news and returns a message"""
    news_to_return = {}
    news_to_return.update({"game": get_game_name_by_id(news["appid"])})
    news_to_return.update({"title": news["title"]})
    news_to_return.update({"url": news["url"]})
    news_to_return.update({"date": datetime.fromtimestamp(news["date"])})
    # new_content = filter_contents(crop_content(news['contents']))
    # news_to_return.update({'content' : new_content})
    return create_message(news_to_return)


def create_message(news):
    """Function that creates the message to send"""
    game_name = "Game news for " + news["game"] + "\n"
    news_url = '<a href ="' + news["url"] + '">Check full news here</a>' + "\n"
    news_title = "<b>" + news["title"] + "</b>" + "\n\n"
    news_date = "<b>Update date: " + str(news["date"]) + "</b>\n\n"

    return game_name + news_url + news_title + news_date
