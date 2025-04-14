import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv() 

TOKEN = os.getenv("TOKEN")

# Initialize Bot
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f'Bot ist online als {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!Ping'):
        await message.channel.send('Pong!')


bot.run(TOKEN)