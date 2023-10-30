from telegram.ext import *
class Bot():
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(self.token).build()
    def getToken(self):
        return self.token