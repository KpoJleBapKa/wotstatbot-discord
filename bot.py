import discord
from discord.ext import commands
import requests
import asyncio
import atexit

TOKEN = 'token'
WG_API_KEY = 'd889298af2382fa0cfeb010e26874b63' 

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="!wothelp"))

@bot.command(name='wothelp')
async def help(ctx, *args):
    message = (
        f"**|--------------------------------------------------------------------------------|**\n"
        f"**Бот** для відслідковування статистики **World of Tanks**\n"
        f"**Префікс - '!'**\n"
        f"\n"
        f"*Команди: *\n"
        f"**!findstat *'nick_name'* -** дізнатися статистику гравця \n"
        f"**!findclan *'clan_name'* -** дізнатися інформацію про клан \n"
        f"**!gm_battles *'clan_name'* -** дізнатися майбутні бої клану на Глобальній Мапі\n"
        f"**!gm_stat *'clan_name'* -** дізнатися статистику клану на Глобальній Мапі\n"
        f"**!clan_members *'clan_name'* -** дізнатися кількість та статистику гравців клану\n"
        f"**|---------------------------------------------------------------------------------|**\n"
    )

    await ctx.send(message)

@bot.command(name='findstat', help='Вивести статистику гравця гри World of Tanks')
async def find_stat(ctx, *args):
    if not args:
        await ctx.send('Невірно введена команда. Приклад: !findstat KpoJleBapKa')
        return
    
    player_name = ' '.join(args)
    wot_api_url = f'https://api.worldoftanks.eu/wot/account/list/?application_id={WG_API_KEY}&search={player_name}'
    
    try:
        response = requests.get(wot_api_url)
        data = response.json()

        if data is None or 'data' not in data or not data['data']:
            await ctx.send(f"Гравець {player_name} не знайдений.")
            return

        account_id = data['data'][0]['account_id']
        stats_url = f'https://api.worldoftanks.eu/wot/account/info/?application_id={WG_API_KEY}&account_id={account_id}'

        response = requests.get(stats_url)
        stats_data = response.json()

        if stats_data is None or 'data' not in stats_data or str(account_id) not in stats_data['data']:
            await ctx.send(f"Статистика для гравця {player_name} недоступна.")
            return

        stats = stats_data['data'][str(account_id)]['statistics']['all']

        clan_info_url = f'https://api.worldoftanks.eu/wot/clans/accountinfo/?application_id={WG_API_KEY}&account_id={account_id}'
        response = requests.get(clan_info_url)
        clan_data = response.json()

        try:
            clan_name = clan_data['data'][str(account_id)]['clan']['tag']
        except (KeyError, TypeError):
            clan_name = "без клану"

        message = (f"**|----------------------------------------------------------------|**\n"
                   f"**Статистика гравця** *{player_name}*\n"
                   f"**Клан: ** {clan_name}\n"
                   f"**Кількість боїв:** {stats['battles']}\n"
                   f"**% перемог:** {stats['wins'] / stats['battles'] * 100:.2f}%\n"
                   f"**% влучень:** {stats['hits'] / stats['shots'] * 100:.2f}%\n"
                   f"**Середня шкода:** {stats['damage_dealt'] / stats['battles']:.2f}\n"
                   f"**Середній досвід:** {stats['xp'] / stats['battles']:.2f}\n"
                   f"**Максимум знищено за бій:** {stats['max_frags']}\n"
                   f"**Максимальний досвід за бій:** {stats['max_xp']}\n"
                   f"**|----------------------------------------------------------------|**")
        await ctx.send(message)

    except Exception as e:
        await ctx.send(f"Виникла помилка: {str(e)}")



@bot.command(name='findclan', help='Вивести інформацію про клан гри World of Tanks')
async def find_clan(ctx, *args):
    if not args:
        await ctx.send('Невірно введена команда. Приклад: !findclan MANKI')
        return
    
    clan_name = ' '.join(args)
    clan_info_url = f'https://api.worldoftanks.eu/wot/clans/list/?application_id={WG_API_KEY}&search={clan_name}'
    try:
        response = requests.get(clan_info_url)
        clan_data = response.json()

        if clan_data is None or 'data' not in clan_data or not clan_data['data']:
            await ctx.send(f"Клан {clan_name} не знайдений.")
            return

        clan_info = clan_data['data'][0]

        clan_members_url = f'https://api.worldoftanks.eu/wot/clans/info/?application_id={WG_API_KEY}&clan_id={clan_info["clan_id"]}&fields=members'
        response = requests.get(clan_members_url)
        clan_members_data = response.json()

        if clan_members_data is None or 'data' not in clan_members_data or str(clan_info["clan_id"]) not in clan_members_data['data']:
            await ctx.send(f"Інформація про гравців клану {clan_name} недоступна.")
            return

        clan_members = clan_members_data['data'][str(clan_info["clan_id"])]["members"]

        message = (f"**|----------------------------------------------------------------|**\n"
                   f"**Інформація про клан** *{clan_name}*\n"
                   f"**Тег клану:** {clan_info['tag']}\n"
                   f"**Назва клану:** {clan_info['name']}\n"
                   f"**Учасники клану:** {clan_info['members_count']}\n"
                   f"**|----------------------------------------------------------------|**")
        await ctx.send(message)

    except Exception as e:
        await ctx.send(f"Виникла помилка: {str(e)}")

@bot.command(name='gm_battles', help='Вивести інформацію про майбутні бої клану на глобальній карті гри World of Tanks')
async def gm_battles(ctx, clan_tag: str = None):
    if clan_tag is None:
        await ctx.send('Невірно введена команда. Приклад: !gm_battles MANKI')
        return
    try:
        clan_info_url = f'https://api.worldoftanks.eu/wot/clans/list/?application_id={WG_API_KEY}&search={clan_tag}'
        response = requests.get(clan_info_url)
        clan_data = response.json()

        if clan_data is None or 'data' not in clan_data or not clan_data['data']:
            await ctx.send(f"Клан з тегом {clan_tag} не знайдений.")
            return

        clan_info = clan_data['data'][0]

        gm_battles_url = f'https://api.worldoftanks.eu/wot/globalmap/clanbattles/?application_id={WG_API_KEY}&clan_id={clan_info["clan_id"]}'
        response = requests.get(gm_battles_url)
        gm_battles_data = response.json()

        if gm_battles_data is None or 'data' not in gm_battles_data or not gm_battles_data['data']:
            await ctx.send(f"На даний момент у клану **{clan_tag}** бої не виставлені.")
            return

        battles = gm_battles_data['data']

        for battle in battles:
            battle_info = battle['battle']

            if len(battles) == 1:
                message = (f"**|----------------------------------------------------------------|**\n"
                           f"**Майбутній бій клану** *{clan_tag}*\n"
                           f"**Проти якого клану:** {battle_info['opponents'][0]['clan']['tag']}\n"
                           f"**На карті:** {battle_info['map']['name_i18n']}\n"
                           f"**Час бою (за Київським часом):** {battle_info['start_at']} UTC\n"
                           f"**|----------------------------------------------------------------|**")
                await ctx.send(message)
            else:
                message = (f"**|----------------------------------------------------------------|**\n"
                           f"**Майбутній бій клану** *{clan_tag}*\n"
                           f"**Проти якого клану:** {battle_info['opponents'][0]['clan']['tag']}\n"
                           f"**На карті:** {battle_info['map']['name_i18n']}\n"
                           f"**Час бою (за Київським часом):** {battle_info['start_at']} UTC\n"
                           f"**|----------------------------------------------------------------|**")
                await ctx.send(message)

    except Exception as e:
        await ctx.send(f"Виникла помилка: {str(e)}")

@bot.command(name='gm_stat', help='Вивести статистику клану на глобальній карті гри World of Tanks')
async def global_clan(ctx, clan_tag: str = None):
    if clan_tag is None:
        await ctx.send('Невірно введена команда. Приклад: !gm_stat MANKI')
        return
    
    try:
        clan_info_url = f'https://api.worldoftanks.eu/wot/clans/list/?application_id={WG_API_KEY}&search={clan_tag}'
        response = requests.get(clan_info_url)
        clan_data = response.json()

        if clan_data is None or 'data' not in clan_data or not clan_data['data']:
            await ctx.send(f"Клан з тегом {clan_tag} не знайдений.")
            return

        clan_info = clan_data['data'][0]

        global_clan_url = f'https://api.worldoftanks.eu/wot/globalmap/claninfo/?application_id={WG_API_KEY}&clan_id={clan_info["clan_id"]}'
        response = requests.get(global_clan_url)
        global_clan_data = response.json()

        if global_clan_data is None or 'data' not in global_clan_data or not global_clan_data['data']:
            await ctx.send(f"Статистика клану **{clan_tag}** на глобальній карті недоступна.")
            return

        clan_stats = global_clan_data['data'][str(clan_info["clan_id"])]

        message = (f"**|----------------------------------------------------------------|**\n"
                   f"**Статистика клану на глобальній карті** *{clan_tag}*\n"
                   f"**Кількість боїв:** {clan_stats.get('battles', 0)}\n"
                   f"**Кількість територій:** {clan_stats.get('territories', 0)}\n"
                   f"**Кількість перемог:** {clan_stats.get('wins', 0)}\n"
                   f"**|----------------------------------------------------------------|**")
        await ctx.send(message)

    except Exception as e:
        await ctx.send(f"Виникла помилка: {str(e)}")

@bot.command(name='clan_members', help='Вивести таблицю лідерів клану по статистиці у випадкових боях')
async def clan_members(ctx, clan_tag: str = None):
    if clan_tag is None:
        await ctx.send('Невірно введена команда. Приклад: !clan_members MANKI')
        return

    try:
        clan_info_url = f'https://api.worldoftanks.eu/wot/clans/list/?application_id={WG_API_KEY}&search={clan_tag}'
        response = requests.get(clan_info_url)
        clan_data = response.json()

        if clan_data is None or 'data' not in clan_data or not clan_data['data']:
            await ctx.send(f"Клан з тегом {clan_tag} не знайдений.")
            return

        clan_info = clan_data['data'][0]
        clan_id = clan_info["clan_id"]

        clan_members_url = f'https://api.worldoftanks.eu/wot/clans/info/?application_id={WG_API_KEY}&clan_id={clan_id}&fields=members'
        response = requests.get(clan_members_url)
        clan_members_data = response.json()

        if clan_members_data is None or 'data' not in clan_members_data or str(clan_id) not in clan_members_data['data']:
            await ctx.send(f"Інформація про гравців клану {clan_tag} недоступна.")
            return

        clan_members = clan_members_data['data'][str(clan_id)]["members"]
        total_members = len(clan_members)

        if not clan_members:
            await ctx.send(f"В клані {clan_tag} немає гравців.")
            return

        leaderboard_message = (
            f"**Клан \"{clan_tag}\"**\n\n"
            f"Кількість гравців у клані: {total_members}\n\n"
            f"**╟ Нік-нейм, роль, % перемог, середня шкода ╣**"
        )

        for index, member_info in enumerate(clan_members[:100], start=1):
            player_name = member_info['account_name']
            member_id = member_info['account_id']

            player_stats_url = f'https://api.worldoftanks.eu/wot/account/info/?application_id={WG_API_KEY}&account_id={member_id}&fields=statistics.all'
            response = requests.get(player_stats_url)
            player_stats_data = response.json()

            if player_stats_data is None or 'data' not in player_stats_data or str(member_id) not in player_stats_data['data']:
                wins_percent = 0.0
                avg_damage = 0.0
            else:
                stats = player_stats_data['data'][str(member_id)]['statistics']['all']
                battles = stats['battles']

                wins_percent = (stats['wins'] / battles * 100) if battles > 0 else 0.0
                avg_damage = (stats['damage_dealt'] / battles) if battles > 0 else 0.0

            leaderboard_message += (
                f"\n**{player_name}** - *{member_info['role']}*  -  **{wins_percent:.2f}%**  -  **{avg_damage:.2f}**"
            )

            if index % 10 == 0 or index == len(clan_members):
                await ctx.send(leaderboard_message)
                leaderboard_message = ""

    except Exception as e:
        await ctx.send(f"Виникла помилка: {str(e)}")

bot.run(TOKEN)