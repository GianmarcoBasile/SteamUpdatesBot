import unittest

from unittest.mock import patch
from main import bot_instance as bot
from bot import Bot
from main import main


class TestMain(unittest.TestCase):
    def test_main(self):
        self.assertTrue(isinstance(bot, Bot))
