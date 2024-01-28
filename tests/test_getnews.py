import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Message, Update
from telegram.ext import CallbackContext
from src.commands import getNews
from telegram.constants import ParseMode


class TestGetNews(unittest.IsolatedAsyncioTestCase):
    async def test_getnews_wrong_args(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = [""]
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        await getNews(update, context)
        message.reply_text.assert_called_once_with(
            "The correct syntax for this command is: /getnews"
        )

    async def test_getnews(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = []
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        with patch("src.commands.get_games_record") as mock_get_games_record:
            mock_get_games_record.return_value = {"games": {"0": "counter-strike 2"}}
            with patch("src.commands.jsonify") as mock_json:
                mock_json.return_value = {
                    "appnews": {"newsitems": {"title:": "test_title"}}
                }
                with patch("src.commands.parser") as mock_get_news:
                    mock_get_news.return_value = 'Game news for counter-strike 2\n<a href ="url">Check full news here</a>\n<b>title</b>\n\n<b>Update date: 1970-01-01 01:00:01</b>\n\n'
                    await getNews(update, context)
        message.reply_text.assert_called_once_with(
            'Game news for counter-strike 2\n<a href ="url">Check full news here</a>\n<b>title</b>\n\n<b>Update date: 1970-01-01 01:00:01</b>\n\n',
            parse_mode=ParseMode.HTML,
        )
