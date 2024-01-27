import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from telegram import Message, Update
from telegram.ext import CallbackContext
from src.commands import getNews


class TestGetNews(unittest.IsolatedAsyncioTestCase):
    @pytest.mark.asyncio
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
