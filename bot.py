'''
Code written by Jason You.
This is a simple python discord bot I made to send 
commands within my discord server.
'''

# Imports
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Initialize intents
intents = discord.Intents.default()
intents.message_content = True

# Load env file
load_dotenv()
# Get environment variable for the access token
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

# Initialize client (bot command is "$")
client = commands.Bot(command_prefix="$", intents=intents)

# Events that occur based on command given
@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def hello(ctx):
    await ctx.send("Bonjour!")

@client.command()
async def yogi(ctx):
    await ctx.send("I love donuts!")

    
@client.command()
async def oops(ctx):
    await ctx.send("D'OH!")
    


client.run(ACCESS_TOKEN)