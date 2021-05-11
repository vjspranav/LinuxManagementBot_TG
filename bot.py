# -*- coding: utf-8 -*-
"""
Created on Wed May 12 01:21:29 2021

@author: vjspranav
"""

import logging
import os
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, ConversationHandler
from functools import wraps
import requests
import json

config={}
with open("config.json") as json_config_file:
    config = json.load(json_config_file)
    
token = config["telegram"]["token"]

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

bot = telegram.Bot(token=token)
print(bot.get_me())
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    user_id = update.effective_chat.id
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! Welcome to the Jenkins bot.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def main():
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()