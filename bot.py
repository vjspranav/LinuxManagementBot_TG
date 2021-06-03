# -*- coding: utf-8 -*-
"""
Created on Wed May 12 01:21:29 2021

@author: vjspranav
"""

import logging
import os
import telegram
import requests
import json
from telegram.ext import Updater
from telegram.ext import CommandHandler, ConversationHandler

# Custom imports
from userHandler import add, uadd, suadd
from userFunctions import storage
from jenkins import build, set

config={}
with open("config.json") as json_config_file:
    config = json.load(json_config_file)

token = config["telegram"]["token"]
jenkins_url = config["jenkins"]["host"]
jenkins_user = config["jenkins"]["user"]
jenkins_pass = config["jenkins"]["pass"]

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

bot = telegram.Bot(token=token)
print(bot.get_me())
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! Welcome to the Linux Management Bot.")

functions = [start, suadd, uadd, add, storage, build, set]
for function in functions:
    handler = CommandHandler(function.__name__, function)
    dispatcher.add_handler(handler)

def main():
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
