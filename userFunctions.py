import subprocess
import os
import json
from telegram.ext.dispatcher import run_async
from restrictions import user_restricted, linux_users


def user_exists(username):
    '''
    Function to check if user exists in linux
    '''
    if os.path.exists('/home/' + username):
        return True
    return False

def del_link(uid):
    linux_users = {}
    with open("users.json") as json_config_file:
        linux_users = json.load(json_config_file)
    deleted = linux_users.pop(str(uid))
    with open("users.json", "w") as json_config_file:
        json.dump(linux_users, json_config_file, indent=4)
    return deleted

def check_user_exists(update, context, uid):
    '''
    Function to check all pre conditoins on whether to allow a user to run a program or not
    '''
    with open("users.json") as json_config_file:
        linux_users = json.load(json_config_file)
    if str(uid) not in linux_users.keys():
        context.bot.send_message(chat_id=update.effective_chat.id, text="User not linked to any linux user")
        return False
    user = linux_users[str(uid)]['linux_username']
    if not user_exists(user):
        sent = context.bot.send_message(chat_id=update.effective_chat.id, text="User " + user + " no longer exists in database, removing link")
        deleted=del_link(uid)
        sent.edit_text('Deleted Link of user @' + deleted['tg_username'] + ' with linux user ' + deleted['linux_username'] + '\nAs the user no longer exists')
        return False
    return True

def du(path):
    """disk usage in human readable format (e.g. '2,1GB')"""
    #output = subprocess.check_output("du -sh " + path, shell=True)
    #return output.decode('utf-8').split()[0]
    return subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')

@user_restricted
def storage(update, context):
    uid = update.effective_user.id
    if not check_user_exists(update, context, uid):
        return
    with open("users.json") as json_config_file:
        linux_users = json.load(json_config_file)
    user = linux_users[str(uid)]['linux_username']

    sent = context.bot.send_message(chat_id=update.effective_chat.id, text="Calculating size occupied by user " + user)
    size = du('/home/' + user)
    sent.edit_text("Size of " +  user + " home directory on server: " + str(size) )
    context.bot.send_message(chat_id=update.effective_chat.id, text="Size of " +  user + " home directory on server: " + str(size))

@user_restricted
def request(update, context):
    uid = update.effective_user.id
    # with open("users.json") as json_config_file:
    #     linux_users = json.load(json_config_file)
    # user = linux_users[str(uid)]['linux_username']

    commands = ' '.join(update.message.text.split(' ')[1:])
    if len(commands) != 0:
        commands = commands.split(',')
    request_commands = {}
    # If exists read request_commands.json
    if os.path.exists('request_commands.json'):
        with open("request_commands.json", 'r') as json_config_file:
            request_commands = json.load(json_config_file)
    # If no commands given, show all commands
    if len(commands) == 0:
        # request_commands is a dict of user: list
        if str(uid) in request_commands:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Your requested commands are\n" + '\n'.join(request_commands[str(uid)]) + '\nPlease contact admin to get approval')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="You have no requested commands to be run")
        return

    if str(uid) not in request_commands.keys():
        print(str(uid) + " not in request_commands")
        request_commands[str(uid)] = []
    
    request_commands[str(uid)].extend(commands)
    with open("request_commands.json", "w") as json_config_file:
        json.dump(request_commands, json_config_file, indent=4)
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Your requested commands are\n" + '\n'.join(request_commands[str(uid)]) + '\nPlease contact admin to get approval')
