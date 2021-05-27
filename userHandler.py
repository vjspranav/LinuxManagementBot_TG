from restrictions import user_restricted, superuser_restricted, linux_users, restricted
from userFunctions import user_exists
from os import path
import json

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
    if not user_exists(luname):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Username does not have a homedir on server")        
        return 

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