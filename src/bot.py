# pylint: skip-file
"""Module providing Bot API."""

from telegram.ext import Application
class Bot():
    """Provides the bot API."""
    def __init__(self, token):
        """Bot Constructor."""
        self.token = token
        self.application = Application.builder().token(self.token).build()
    def get_token(self):
        """Return the API Token."""
        return self.token
