import unittest
from main import bot_instance as bot
from bot import Bot


class TestMain(unittest.TestCase):
    def test_main(self):
        self.assertTrue(isinstance(bot, Bot))
