# LinuxManagementBot_TG
A simple bot to help manage users on Linux

## Pre-requisites
* Install the following library using pip
```
pip install python-telegram-bot
```
## Setup
* Open config.json and edit as follows, telegram bot token obtained from botfather  
```
{
  "telegram": {
    "token": "1234xyz:abcdefghj"
  }
}
```
* Open restricted.json, add the main user who has control from beginning as follows  
Ex: Username is **vjspranav** and id is **12345**
```
{
    "user": {
    },
    "superuser": {
        "vjspranav" : "12345"
    }
}
```

## Explanation
* config.json contains your telegram token
* restricted.json contains which users the bot is restricted to
* users.json contains the links from tguser to linux user in server (to be added through commands)
* The restricted.json can be edited while the bot is running, the details are dynamically updated.

## Available functions
### /start 
* Welcome message  
### /uadd
* Adds the user of tagged message to users list.  
> TODO: Do no allow bots to be added  
### /suadd
* Adds the user of tagged message to superusers list and also users list if not already existing.  
> TODO: Do no allow bots to be added  
### /add <linux username>
* Links the user of tagged message to the linux username mentioned, dooes not work if mentioned user already is linked  
> TODO: Make sure linux user exists.  