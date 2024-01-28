import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Message, Update
from telegram.ext import CallbackContext
from src.commands import saleOnGames


class TestSaleOnGames(unittest.IsolatedAsyncioTestCase):
    async def test_saleongames_wrong_args(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        message = MagicMock(spec=Message)
        update.message = message
        context.args = [""]
        message.from_user.username = "test_user"
        message.reply_text = AsyncMock()
        await saleOnGames(update, context)
        message.reply_text.assert_called_once_with(
            "The correct syntax for this command is: /checksales"
        )

    async def test_saleongames_free(self):
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
                    "730": {"success": True, "data": {"is_free": True}}
                }
                await saleOnGames(update, context)
        message.reply_text.assert_called_once_with("The game counter-strike 2 is free")

    async def test_saleongames_notonsale(self):
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
                    "730": {
                        "success": True,
                        "data": {
                            "is_free": False,
                            "price_overview": {
                                "initial": 10,
                                "final": 10,
                                "final_formatted": "10€",
                            },
                        },
                    }
                }
                await saleOnGames(update, context)
        message.reply_text.assert_called_once_with(
            "The game counter-strike 2 is not on sale. It costs 10€"
        )

    async def test_saleongames_onsale(self):
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
                    "730": {
                        "success": True,
                        "data": {
                            "is_free": False,
                            "price_overview": {
                                "initial": 10,
                                "final": 5,
                                "initial_formatted": "10€",
                                "final_formatted": "5€",
                            },
                        },
                    }
                }
                await saleOnGames(update, context)
        message.reply_text.assert_called_once_with(
            "The game counter-strike 2 is on sale for 5€ instead of 10€"
        )
