import discord
from discord.ext import commands

client = commands.Bot(command_prefix="$")

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
    


client.run("")