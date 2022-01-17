# DiscordModBot

Discord moderation bot working on Sqlite3, discord.py.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
pip install -r requirements.txt
```

## Usage
For the bot to work correctly, you need to substitute your values ​​in ***Config.py.***   

```python
#Config.py
Token = "Enter your token"
OWNERID = Enter your id
```     

And some values in ***someimportantthings.py.***.
    
```python
#someimportantthings
GIRLS_ROLE = Enter your girls role id
BOYS_ROLE = Enter your boys role id
TRUSTED_CHANNELS = (Enter two or more channel id, where you want use commands)
VERIFY_ROLE = Enter your verify role
CHANNEL_FOR_LOGS = Enter channel id, where you want collect logs
SERVER_ID = Enter id of your guild
MUTE_ROLE = Enter your mute role id
```    
> If you are missing any roles, you need to create them on guild settings.

***To get the id of a role, guild or channel, you need to right-click on the desired object.***

<p align="center">
  <img src="https://cdn.discordapp.com/attachments/930560944835293214/930901516129275975/unknown.png"/>
</p>

## Commands
Used **HotSwap**, it's means you can do changes on cogs files without shutdown bot.    ​
* Cog loader commands:    
  * !load **[cogname]** - you can do it, if you want to load new  cog;    
  * !unload **[cogname]** - you can do it, if you want to unload cog;    
  *  !reload **[cogname]** - you can do it, if you want to reload new  cog.
* User commands:    
  * !profile - displays user information;    
  * !status - you can create your own status.
* Mod commands:
  * !clear **[value]** - deletes the required number of messages;
  * !ban **[member] [reason]** - bans a user with a reason;
  * !kick **[member] [reason]** - kicks a user with a reason;
  * !mute **[member] [time] [reason]** - mute the user for a specified time, with a reason ***(can mute: only text, only voice, text&voice)***;
  * !gender **[member]** - gives the option to give one of two binary genders ***(If you want to assign a non-binary gender, use the !give command)***;
  * !swap **[member]** - makes it possible to change one of the gender roles to another according to the binary system ***(If you want to assign a non-binary gender, use the !give command)***;
  * !give **[member] [role]** - gives the user a role ***(before issuing, make sure that the role such a role exists
!)***;
  * !take **[member] [role]** - takes the role from the user ***(before issuing, make sure that the user has such a role
!)***.
* Role commands:
  * !role create **[rolename]** - creates a role on the guild with the **[rolename]** specified by the user;
  * !role manage - opens the interaction menu with the previously created role ***(you can: delete your role, change color).***


## ErrorHandler
If you catch some problem you need to unload ***ErrorHandler***. When you do this, you will monitor the error in the console.

## Member_join & Member_leave handler
When a new user joins the guild, the bot gives him a verify role and leaves a log.    

Also when the user leaves the server it is logged.
## logging
**Every** moderation action performed using the bot is logged.    
***Example:***    
<p align="center">
  <img src="https://media.discordapp.net/attachments/930560944835293214/932599473073455134/unknown.png"/>
</p>

## Futures
* ***Some interesting...***
## <blank>
<h3><p align="center">Attention</p></h3>
<h3><p align="center">If you see this message:</p></h3>
<p align="center">
  <img src="https://cdn.discordapp.com/attachments/930134889225912323/930906569355427870/unknown.png"/>
</p>
<h3><p align="center">You need to check OWNERID in Config.py for correct data</p></h3>
