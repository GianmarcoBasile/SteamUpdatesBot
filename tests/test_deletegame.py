import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from telegram import Message, Update
from telegram.ext import CallbackContext
from src.commands import deleteGame


class TestDeleteGame(unittest.IsolatedAsyncioTestCase):
    async def test_deleteGame_successful(self):
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
                mock_get_games_record.return_value = {
                    "games": {"0": "counter-strike 2"}
                }
                await deleteGame(update, context)
        message.reply_text.assert_called_once_with(
            "Game counter-strike 2 deleted from the list"
        )

    async def test_deleteGame_no_args(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = []
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        await deleteGame(update, context)
        message.reply_text.assert_called_once_with(
            "The correct syntax for this command is: /deletegame <game_name>"
        )

    async def test_deleteGame_wrong_args(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = ["asdasd"]
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        with patch("src.commands.get_games_record") as mock_get_games_record:
            mock_get_games_record.return_value = {"games": {"0": "counter-strike 2"}}
            await deleteGame(update, context)
        message.reply_text.assert_called_once_with("The game is not in the list")
