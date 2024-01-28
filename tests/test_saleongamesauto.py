import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram.ext import CallbackContext
from src.commands import saleOnGamesAuto


class TestSaleOnGamesAuto(unittest.IsolatedAsyncioTestCase):
    async def test_saleongamesauto_free(self):
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
            with patch("src.commands.jsonify") as mock_json:
                mock_json.return_value = {
                    "730": {"success": True, "data": {"is_free": True}}
                }
                await saleOnGamesAuto(context)
        context.bot.send_message.assert_called_once_with(
            1, "The game counter-strike 2 is free"
        )

    async def test_saleongamesauto_notonsale(self):
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
            with patch("src.commands.jsonify") as mock_json:
                mock_json.return_value = {
                    "730": {
                        "success": True,
                        "data": {
                            "is_free": False,
                            "price_overview": {"initial": 10, "final": 10},
                        },
                    }
                }
                await saleOnGamesAuto(context)
        context.bot.send_message.assert_called_once_with(
            1, "The game counter-strike 2 is not on sale"
        )

    async def test_saleongamesauto_sale(self):
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
            with patch("src.commands.jsonify") as mock_json:
                mock_json.return_value = {
                    "730": {
                        "success": True,
                        "data": {
                            "is_free": False,
                            "price_overview": {
                                "initial": 10,
                                "final": 5,
                                "final_formatted": "5,00€",
                            },
                        },
                    }
                }
                await saleOnGamesAuto(context)
        context.bot.send_message.assert_called_once_with(
            1, "The game counter-strike 2 is on sale for 5,00€"
        )
