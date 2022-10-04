from restrictions import user_restricted, superuser_restricted, linux_users, restricted
from userFunctions import user_exists, del_link
from os import path, system
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
        context.bot.send_message(chat_id=update.effective_chat.id, text="Already a sudo user")

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
    if not user_exists(luname):
        context.bot.send_message(chat_id=update.effective_chat.id, text="User doesn't exist on server")
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

@superuser_restricted
def reject_command(update, context):
    rejections = update.message.text.split(" ")[1:]
    # user = linux_users[str(uid)]['linux_username']
    request_commands = {}
    with open("request_commands.json") as json_config_file:
        request_commands = json.load(json_config_file)

    for rejection in rejections:
        try:
            ind = int(rejection[0])
            c_ind = int(rejection[1])
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid rejection " + rejection)
            continue
        
        if ind > len(request_commands.keys()):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid rejection " + rejection)
            continue
        key = list(request_commands.keys())[ind]        
        if c_ind > len(request_commands[key]):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid rejection " + rejection)
            continue
        

        del request_commands[key][c_ind]
        if len(request_commands[key]) == 0:
            del request_commands[key]
        context.bot.send_message(chat_id=update.effective_chat.id, text="Rejected " + rejection)
    with open("request_commands.json", "w") as json_config_file:
        json.dump(request_commands, json_config_file, indent=4)

@superuser_restricted
def approve_command(update, context):
    approvals = update.message.text.split(" ")[1:]
    request_commands = {}
    with open("users.json") as json_config_file:
        linux_users = json.load(json_config_file)
    with open("request_commands.json") as json_config_file:
        request_commands = json.load(json_config_file)
    if len(approvals) == 0:
        # Send all requests
        if len(request_commands) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No requests")
            return
        msg = ""
        ind=0
        c_ind=0
        for key in request_commands.keys():
            msg += "User: " + linux_users[str(key)]['linux_username'] + "\n"
            c_ind=0
            for command in request_commands[key]:
                msg += "  " + str(ind) + str(c_ind) + " " + command + "\n"
                c_ind+=1
            ind+=1
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        return
    for approval in approvals:
        if len(approval) != 2:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid approval " + approval)
            continue
        try:
            ind = int(approval[0])
            c_ind = int(approval[1])
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid approval " + approval)
            continue
        if ind >= len(request_commands.keys()):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid approval " + approval)
            continue
        key = list(request_commands.keys())[ind]
        if c_ind >= len(request_commands[key]):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid approval " + approval)
            continue
        command = request_commands[key][c_ind]
        if 'rm' in command:
            context.bot.send_message(chat_id=update.effective_chat.id, text="rm command not allowed, Please use /del")
            continue
        system(command)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Command executed: " + command)
        request_commands[key].remove(command)
        if len(request_commands[key]) == 0:
            del request_commands[key]

    with open("request_commands.json", "w") as json_config_file:
        json.dump(request_commands, json_config_file, indent=4)


@superuser_restricted
def run(update, context):
    command = update.message.text.split(" ")[1]
    if 'rm' in command:
        context.bot.send_message(chat_id=update.effective_chat.id, text="rm not allowed")
        return
    
    system(command)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Command executed")