# DiscordModBot

Discord moderation bot working on Sqlite3, discord.py

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

And some values in ***someimportantthings.py.*** 
    
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
If you are missing any roles, you need to create them on guild settings.

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

## ErrorHandler
If you catch some problem you need to unload ***ErrorHandler***. When you do this, you will monitor the error in the console

## Futures
* Mod commands **[In working]**:
  * kick;
  * mute;
  * ban;
  * take role; 
  * give role.

* Role and Channel commands **[In working]**:
  * Member_join & Member_leave handler;
  * private role creator;
  * private role manager.

* ***And some interesting...***
## <blank>
<h3><p align="center">Attention</p></h3>
<h3><p align="center">If you see this message:</p></h3>
<p align="center">
  <img src="https://cdn.discordapp.com/attachments/930134889225912323/930906569355427870/unknown.png"/>
</p>
<h3><p align="center">You need to check OWNERID in Config.py for correct data</p></h3>
