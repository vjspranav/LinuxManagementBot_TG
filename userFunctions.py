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
