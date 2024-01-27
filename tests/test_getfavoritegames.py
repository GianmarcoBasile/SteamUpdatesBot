import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from telegram import Message, Update
from telegram.ext import CallbackContext
from src.commands import getFavoriteGames


class TestGetFavoriteGamesList(unittest.IsolatedAsyncioTestCase):
    async def test_getfavoritegames_successful(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = []
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        with patch("src.commands.get_games_record") as mock_get_games_record:
            mock_get_games_record.return_value = {"games": {"0": "counter-strike 2"}}
            await getFavoriteGames(update, context)
        message.reply_text.assert_called_once_with("Favorite Games: counter-strike 2")

    async def test_getfavoritegames_wrong_args(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = [""]
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        await getFavoriteGames(update, context)
        message.reply_text.assert_called_once_with(
            "The correct syntax for this command is: /favoritegames"
        )
