import discord
from discord.ext import commands
import os
import requests

# Set bot token and Brawl Stars API token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
BRAWL_STARS_TOKEN = os.getenv('BRAWL_STARS_TOKEN')

# Define intents
intents = discord.Intents.default()

# Set command prefix
bot = commands.Bot(command_prefix='/', intents=intents)

# Brawl Stars API endpoint
API_URL = 'https://api.brawlstars.com/v1/'

# Replace 'your_brawl_stars_token_here' with your Brawl Stars API token
HEADERS = {
    'Authorization': f'Bearer {BRAWL_STARS_TOKEN}',
    'Accept': 'application/json'
}

# Database to store Brawl Stars account with Discord ID
account_database = {}

# Function to fetch brawlers data from Brawl Stars API
def get_brawlers():
    response = requests.get(API_URL + 'brawlers', headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to fetch club data from Brawl Stars API
def get_club(tag):
    response = requests.get(API_URL + f'clubs/{tag}', headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to fetch brawler icon URL from Brawl Stars API
def get_brawler_icon_url(name):
    brawlers_data = get_brawlers()
    if brawlers_data:
        for brawler in brawlers_data['items']:
            if brawler['name'].lower() == name.lower():
                return brawler['imageUrl']
    return None

# Command to fetch and display brawlers data
@bot.command()
async def brawlers(ctx):
    brawlers_data = get_brawlers()
    if brawlers_data:
        await ctx.send(brawlers_data)
    else:
        await ctx.send('Failed to fetch brawlers data.')

# Command to fetch and display club data
@bot.command()
async def club(ctx, tag):
    club_data = get_club(tag)
    if club_data:
        await ctx.send(club_data)
    else:
        await ctx.send(f'Failed to fetch club data for tag {tag}.')

# Command to fetch and display brawler icon
@bot.command()
async def icon(ctx, brawler_name):
    icon_url = get_brawler_icon_url(brawler_name)
    if icon_url:
        await ctx.send(icon_url)
    else:
        await ctx.send(f'Failed to find icon for brawler {brawler_name}.')

# Command to save Brawl Stars account with Discord ID
@bot.command()
async def save(ctx, brawl_stars_id):
    account_database[ctx.author.id] = brawl_stars_id
    await ctx.send(f'Brawl Stars account saved for user {ctx.author.name}.')

# Command to display custom help message
@bot.command()
async def myhelp(ctx):
    help_message = """
    Available Commands:
    /brawlers - Fetch information about brawlers.
    /club [tag] - Fetch information about a club using its tag.
    /icon [brawler_name] - Fetch the icon URL of a brawler.
    /save [brawl_stars_id] - Save your Brawl Stars account with your Discord ID.
    /myhelp - Display this help message.
    """
    await ctx.send(help_message)

# Run the bot
bot.run(BOT_TOKEN)
