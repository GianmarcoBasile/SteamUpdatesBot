import unittest
from unittest.mock import patch
from main import bot_instance as bot
from bot import Bot


class TestMain(unittest.TestCase):
    def test_main(self):
        with patch("src.main.API_KEY") as mock_api_key:
            mock_api_key.return_value = "test_api_key"
        self.assertTrue(isinstance(bot, Bot))
