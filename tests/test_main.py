import unittest
from pytest import MonkeyPatch
from main import bot_instance as bot
from bot import Bot


class TestMain(unittest.TestCase):
    def test_main(self):
        monkeypatch = MonkeyPatch()
        monkeypatch.setenv("API_KEY", "test_api_key")
        self.assertTrue(isinstance(bot, Bot))
