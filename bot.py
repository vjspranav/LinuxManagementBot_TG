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
restricted={}
linux_users={}

token = config["telegram"]["token"]
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

bot = telegram.Bot(token=token)
print(bot.get_me())
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

def superuser_restricted(func):
    """Restrict usage of func to allowed users only and replies if necessary"""
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        with open("restricted.json") as json_config_file:
            restricted = json.load(json_config_file)
        user_id = update.effective_user.id
        if str(user_id) not in restricted['superuser'].values():
            print(user_id, " is not in superuser")
            print("WARNING: Unauthorized access denied for {}.".format(user_id))
            update.message.reply_text('Not Superuser, incident will be recorded')
            return  # quit function
        return func(update, context, *args, **kwargs)
    return wrapped

def user_restricted(func):
    """Restrict usage of func to allowed users only and replies if necessary"""
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        with open("restricted.json") as json_config_file:
            restricted = json.load(json_config_file)
        user_id = update.effective_user.id
        if str(user_id) not in restricted['user'].values():
            print(user_id, " is not in accessible users")
            print("WARNING: Unauthorized access denied for {}.".format(user_id))
            update.message.reply_text('User disallowed.')
            return  # quit function
        return func(update, context, *args, **kwargs)
    return wrapped


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! Welcome to the Linux Management Bot.")

@superuser_restricted
def suadd(update, context):
    send="User successfully promoted"
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id  
        uname = update.message.reply_to_message.from_user.username
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No user tagged")
        return
    tconfig = {}    
    with open("restricted.json") as json_config_file:
        tconfig = json.load(json_config_file)      
    if str(uid) not in tconfig['superuser'].values():
        tconfig['superuser'][uname] = str(uid)
        if str(uid) not in tconfig['user'].values():
            tconfig['user'][uname] = str(uid)
            send="User added and promoted"
        with open("restricted.json", "w") as json_config_file:
            tconfig = json.dump(tconfig, json_config_file, indent=4)      
        context.bot.send_message(chat_id=update.effective_chat.id, text=send)  
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Already Superuser")  

@superuser_restricted
def uadd(update, context):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id  
        uname = update.message.reply_to_message.from_user.username
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No user tagged")
        return
    tconfig = {}    
    with open("restricted.json") as json_config_file:
        tconfig = json.load(json_config_file)      
    if str(uid) not in tconfig['user'].values():
        tconfig['user'][uname] = str(uid)
        with open("restricted.json", "w") as json_config_file:
            tconfig = json.dump(tconfig, json_config_file, indent=4)      
        context.bot.send_message(chat_id=update.effective_chat.id, text="User added")  
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Already user")  


@superuser_restricted
def add(update, context):
    inp = update.message.text.split(" ")
    if len(inp) < 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Username not provided")        
        return 
    luname = inp[1]
    ## To do
    # Add check if username exists    
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id  
        uname = update.message.reply_to_message.from_user.username
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No user tagged")
        return
    send="User " + uname + " successfully linked to " + luname
    tconfig = {}    
    with open("restricted.json") as json_config_file:
        tconfig = json.load(json_config_file)      
    if str(uid) not in tconfig['superuser'].values():
        if str(uid) not in tconfig['user'].values():
            context.bot.send_message(chat_id=update.effective_chat.id, text="Tagged user doesn't exist in database either use /uadd or /suadd")  
            return
    tconfig = {}    
    with open("users.json") as json_config_file:
        tconfig = json.load(json_config_file)
    if str(uid) in tconfig.keys():
        context.bot.send_message(chat_id=update.effective_chat.id, text="Already linked to a linux user")
        return
    tconfig[str(uid)] = {
            "tg_username" : uname,
            "linux_username" : luname,
            "u_id": str(uid)
        }
    with open("users.json", "w") as json_config_file:
         json.dump(tconfig, json_config_file, indent=4)
    context.bot.send_message(chat_id=update.effective_chat.id, text=send)  
 

functions = [start, suadd, uadd, add]
for function in functions:
    handler = CommandHandler(function.__name__, function)
    dispatcher.add_handler(handler)

def main():
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()