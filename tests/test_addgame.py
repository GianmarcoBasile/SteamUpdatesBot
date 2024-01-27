import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from telegram import Message, Update
from telegram.ext import CallbackContext
from src.commands import addGame


class TestAddGame(unittest.IsolatedAsyncioTestCase):
    async def test_addGame_no_args(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = []
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        await addGame(update, context)
        message.reply_text.assert_called_once_with(
            "The correct syntax for this command is: /addgame <game_name>"
        )

    async def test_addGame_wrong_args_suggestion(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = ["counter strike"]
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        await addGame(update, context)
        self.assertRegex(
            message.reply_text.call_args[0][0],
            r"Game not found. Maybe you meant: (.*)counter-strike(.*)",
        )

    async def test_addGame_wrong_args_no_suggestion(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = ["asdasd"]
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        await addGame(update, context)
        message.reply_text.assert_called_once_with("The game is not a steam game")

    async def test_addGame_twice(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = ["counter-strike", "2"]
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        with patch("src.commands.get_games_record") as mock_get_games_record:
            mock_get_games_record.return_value = {"games": {"0": "counter-strike 2"}}
            await addGame(update, context)
        message.reply_text.assert_called_once_with("The game is already in the list")

    async def test_addGame_successful(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = ["counter-strike", "2"]
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        with patch("src.commands.get_games_record") as mock_get_games_record:
            with patch("src.commands.update_games_record") as mock_update_games_record:
                mock_update_games_record.return_value = None
                mock_get_games_record.return_value = {"games": {}}
                await addGame(update, context)
        message.reply_text.assert_called_once_with(
            "Game counter-strike 2 added to the list"
        )
