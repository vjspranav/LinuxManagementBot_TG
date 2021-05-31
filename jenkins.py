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
