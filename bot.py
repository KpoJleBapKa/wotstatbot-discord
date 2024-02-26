import discord
from discord.ext import commands
import requests

TOKEN = 'token'
WG_API_KEY = 'd889298af2382fa0cfeb010e26874b63' 

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='findstat')
async def find_stat(ctx, *args):
    print(ctx.message.content)
    if not args:
        await ctx.send('Невірно введена команда. Приклад: !findstat KpoJleBapKa')
        return
    
    player_name = ' '.join(args)
    wot_api_url = f'https://api.worldoftanks.eu/wot/account/list/?application_id={WG_API_KEY}&search={player_name}'
    
    try:
        response = requests.get(wot_api_url)
        data = response.json()
        
        account_id = data['data'][0]['account_id']
        stats_url = f'https://api.worldoftanks.eu/wot/account/info/?application_id={WG_API_KEY}&account_id={account_id}'

        response = requests.get(stats_url)
        stats_data = response.json()

        if 'data' in stats_data:
            stats = stats_data['data'][str(account_id)]['statistics']['all']
            message = (f"**Статистика гравця** *{player_name}*:\n"
                       f"**Кількість боїв:** {stats['battles']}\n"
                       f"**% перемог:** {stats['wins'] / stats['battles'] * 100:.2f}%\n"
                       f"**% влучень:** {stats['hits'] / stats['shots'] * 100:.2f}%\n"
                       f"**Середня шкода:** {stats['damage_dealt'] / stats['battles']:.2f}\n"
                       f"**Середній досвід:** {stats['xp'] / stats['battles']:.2f}\n"
                       f"**Максимум знищено за бій:** {stats['max_frags']}\n"
                       f"**Максимальний досвід за бій:** {stats['max_xp']}")
        else:
            message = f"**Гравець {player_name} не знайдений.**"

        await ctx.send(message)

    except Exception as e:
        await ctx.send(f"Виникла помилка: {str(e)}")

bot.run(TOKEN)
