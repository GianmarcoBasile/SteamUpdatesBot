import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram.ext import CallbackContext
from src.commands import getNewsAuto
from telegram.constants import ParseMode


class TestGetNewsAuto(unittest.IsolatedAsyncioTestCase):
    async def test_getnewsauto(self):
        context = MagicMock(spec=CallbackContext)
        context.args = []
        context.bot.send_message = AsyncMock()
        with patch("src.commands.find_users") as mock_find_users:
            mock_find_users.return_value = [
                {
                    "chat_id": 1,
                    "user": "test_user",
                    "games": {"0": "counter-strike 2"},
                }
            ]
            with patch("src.commands.parser") as mock_parser:
                mock_parser.return_value = 'Game news for counter-strike 2\n<a href ="url">Check full news here</a>\n<b>title</b>\n\n<b>Update date: 1970-01-01 01:00:01</b>\n\n'
                await getNewsAuto(context)
        context.bot.send_message.assert_called_once_with(
            1,
            'Game news for counter-strike 2\n<a href ="url">Check full news here</a>\n<b>title</b>\n\n<b>Update date: 1970-01-01 01:00:01</b>\n\n',
            parse_mode=ParseMode.HTML,
        )
