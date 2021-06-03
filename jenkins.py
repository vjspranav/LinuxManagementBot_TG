import requests

from restrictions import user_restricted, linux_users

def jenbuild(token, job, jenkins_params, buildWithParameters = True):
    jenkins_job_name =job
    jenkins_params['token'] = token
    jenkins_params['job'] = job
    try:
        auth = (jenkins_user, jenkins_pass)
        crumb_data = requests.get("{0}/crumbIssuer/api/json".format(jenkins_url), auth = auth, headers={'content-type': 'application/json'})
        if str(crumb_data.status_code) == "200":

                if buildWithParameters:
                        data = requests.get("{0}/job/{1}/buildWithParameters".format(jenkins_url, jenkins_job_name), auth=auth, params=jenkins_params, headers={'content-type': 'application/json', 'Jenkins-Crumb':crumb_data.json()['crumb']})
                else:
                        data = requests.get("{0}/job/{1}/build".format(jenkins_url, jenkins_job_name), auth=auth, params=jenkins_params, headers={'content-type': 'application/json', 'Jenkins-Crumb':crumb_data.json()['crumb']})

                if str(data.status_code) == "201":
                 print("Triggered Jenkins job.")
                 return True
                else:
                 print("Failed to trigger Jenkins job.")
                 return False

        else:
                print("Couldn't fetch Jenkins crumb data.")
                raise

    except Exception as e:
        print ("Failed triggering Jenkins job")
        print ("Error: " + str(e))

@user_restricted
def build(update, context):
    inp = update.message.text
    jenkins_job_name ="Job Name"
    pms = inp.split(' ')
    l="Starting Job\n"
    sent=context.bot.send_message(chat_id=update.effective_chat.id, text=l)
    if len(pms)%2 == 0:
        sent.edit_text("Invalid parameter key/value pairs given")
        return

    params={}
    for i in range(1, len(pms), 2):
        params[pms[i]] = pms[i+1]
    print(params)

    for p in params:
        l+="With " + p +" = " + params[p] + "\n"
        sent.edit_text(l)

    success= "\n" + inp + " triggered"
    fail="\nSomething went wrong for job " + inp
    # Generate a random token key and set it for jenkins build and add below
    if jenbuild("jenkinstoken", jenkins_job_name, params, True):
        sent.edit_text(l+success)
    else:
        sent.edit_text(l+fail)

def user_exists(username):
    if os.path.exists('/home/' + username):
        return True
    return False

@user_restricted
def set(update, context):
    uid = update.effective_user.id
    with open("users.json") as json_config_file:
        linux_users = json.load(json_config_file)
    if str(uid) not in linux_users.keys():
        context.bot.send_message(chat_id=update.effective_chat.id, text="User not linked to any linux user")
        return
    user = linux_users[str(uid)]['linux_username']
    if not user_exists(user):
        sent = context.bot.send_message(chat_id=update.effective_chat.id, text="The connected linux username does not exist.\nDeleting link")
        deleted = linux_users.pop(str(uid))
        with open("users.json", "w") as json_config_file:
         json.dump(linux_users, json_config_file, indent=4)
        sent.edit_text('Deleted Link of user @' + deleted['tg_username'] + ' with linux user ' + deleted['linux_username'] + '\nAs the user no longer exists')
        return
    inp = update.message.text
    if len(inp.split(" ")) == 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Dir not provided")
        return
    inp = inp.split(" ")
    command='chown ' + user + ':jenkins /home/' + user + '/%s -R'%(inp[1])
    os.system(command)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Done setting up permissions for %s dir"%(inp[1]))
