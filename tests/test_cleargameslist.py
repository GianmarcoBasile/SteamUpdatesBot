import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from telegram import Message, Update
from telegram.ext import CallbackContext
from src.commands import clearGamesList


class TestClearGamesList(unittest.IsolatedAsyncioTestCase):
    @pytest.mark.asyncio
    async def test_cleargameslist_successful(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = []
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        with patch("src.commands.get_games_record") as mock_get_games_record:
            with patch("src.commands.update_games_record") as mock_update_games_record:
                mock_update_games_record.return_value = None
                mock_get_games_record.return_value = {
                    "games": {"0": "counter-strike 2"}
                }
                await clearGamesList(update, context)
        message.reply_text.assert_called_once_with("Games list cleared")

    @pytest.mark.asyncio
    async def test_cleargameslist_wrong_args(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = [""]
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        await clearGamesList(update, context)
        message.reply_text.assert_called_once_with(
            "The correct syntax for this command is: /cleargameslist"
        )
