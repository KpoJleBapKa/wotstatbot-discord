# WotStat BOT

**This bot will be useful for you if you want to find WOT-players statistic.**<br>

**Bot functions:**
  - Displaying statistic via message

**How to use:**
  - !findstat 'nick_name' - find out the player's statistics
  - !findclan 'clan_name' - find out information about the clan
  - !gm_battles 'clan_name' - find out upcoming clan battles on the Global Map
  - !gm_stat 'clan_name' - find out clan statistics on the Global Map
  - !clan_members 'clan_name' - find out the number and statistics of clan players
  
## FAQ:

1. How do I connect a bot to my Discord server?
You can connect a bot to your server by creating a bot on the Discord developer page (https://discord.com/developers/applications) and giving it the necessary permissions to run on your server. After that, add the bot using the link from the bot settings page.
2. How to start a bot?
To run the bot, you need to call the run method with your bot's token. Example: bot.run('YOUR_TOKEN') 
3. How to configure a bot for another server?
You can customize the bot for a different server by adding new server details to the bot code. To do this, you should add the appropriate entries to the server_data list.
4. Why is the bot not sending information to my server?
Make sure the bot has access to the text feed on your server and that server_data contains the correct settings for your server.
5. How do I delete information sent by a bot?
The bot automatically deletes old messages and updates information. You can delete old messages manually using the !clear command.
6. How can I get more help or contact the bot developer?
You can contact the bot developer by sending a private message on Discord: kpojiebapka.
7. Is this bot open source?
Yes, it is! Use it to your satisfaction!
8. How do I get updates and upgrades for the bot?
The bot is automatically updated with new versions. Just monitor this repository and commits.
