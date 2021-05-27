from functools import wraps
import json

restricted={}
linux_users={}

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
