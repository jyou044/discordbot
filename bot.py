'''
Code written by Jason You.
This is a simple python discord bot I made to have interactions with the yogibot
The photo-caption generation was inspired by https://docs.replit.com/tutorials/discord-meme-maker-bot

V1.0.0
'''

# Imports
import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Initialize intents
intents = discord.Intents.default()
intents.message_content = True

# Load env file
load_dotenv()
# Get environment variable for the access token
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
BOT_ID = os.getenv('BOT_ID')

# Initialize client (bot command is "$")
client = commands.Bot(command_prefix="$", intents=intents)

# Events that occur based on command given
@client.event
async def on_ready():
    print("YogiBot is ready")

# Command that informs the user of the commands they can use
@client.command()
async def yogiHelp(ctx):
    embeded = embed_help()
    await ctx.send(embed=embeded)

# Command to send randomized catch phrase Homer says
@client.command()
async def yogi(ctx):
    await ctx.send(random.choice(["I love donuts!", "Bonjour", "D'OH!"]))


# Command to have user guess a number the yogibot is thinking of
@client.command()
async def guess(ctx):
    count = 0
    flag = 0
    yogiMessage = "I'm thinking of a number between 1 and 20, can you guess the number in five tries?"
    chosenNumber = random.randint(1,20)
    await ctx.send(yogiMessage)
    try:
        while count < 5:
            try:
                print("Count: ", count)
                msg = await client.wait_for("message",
                check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)
                print("User msg received: ", msg.content)
                if int(msg.content) == chosenNumber:
                    flag = 1
                    await ctx.send("Correct! That is the number I guessed")
                    break
                else:
                    count+=1
                    if count < 5:
                        await ctx.send("Sorry that wasn't the number I had in mind!")
            except Exception as e1:
                print("Error: ", e1)
                await ctx.send("Please enter a valid number!")
    except Exception as e:
        print("Error random number:", e)
    if flag == 0:
        await ctx.send("Sorry! The number I chose was "+ str(chosenNumber) + " better luck next time!")

# Command to send picture with user inputted caption
@client.command()
async def photo(ctx):
    yogiMessage = "Homer is having trouble finding a caption for images. Please enter a caption for a randomly generated image. \n *Request times out in 30 seconds!*"
    chosen_file = random.choice(['images/Homer_Simpson.png', 'images/spongebob.png'])
    embeded = discord.Embed(
        title="Yogi's Photo-Caption Generator",
        description= yogiMessage
    )

    # Send embed card to user informing them that they will need to enter a caption for the randomly chosen image
    try:
        embeded.set_image(url='https://i.imgur.com/JIgJNTd.png')
        await ctx.send(embed=embeded)
    except Exception as e:
        print("Error occurred sending embed: ", e)

    # Send image with caption inputted by user
    try:
        msg = await client.wait_for("message",
        check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel, timeout=30)
        print("User msg received: ", msg.content)
        image_modifier(chosen_file, msg.content)
        await ctx.send(file=discord.File("final.png"))
    except Exception as e:
        print("Error", e)
        await ctx.send("Sorry, I didn't get your message in time! Maybe you forgot to press enter?")

# Command to send a randomly selected GIF meme
@client.command()
async def meme(ctx):
    await ctx.send(random.choice(['https://imgur.com/t/homer/dPNFUBP', 'https://imgur.com/t/homer/cFqbFq1', 'https://imgur.com/HbrKEnf',
    'https://giphy.com/gifs/dance-spongebob-bob-nDSlfqf0gn5g4', 'https://giphy.com/gifs/spongebob-squarepants-cehalopod-lodge-5vee7PEK0reww']))


# Command when bot is pinged by the user
@client.event
async def on_message(ctx):
    if str(ctx.content) == BOT_ID:
        await ctx.channel.send('Greetings! Yogibot at your service!')
        await ctx.channel.send(embed=embed_help())
    await client.process_commands(ctx)


def image_modifier(chosen_file, msg):
    base = Image.open(chosen_file).convert("RGBA")
    updated_image = Image.new("RGBA", base.size, (255, 255, 255, 0))
    fnt = ImageFont.truetype("impact.ttf", 30)
    draw = ImageDraw.Draw(updated_image)
    draw.text((10,300), msg,font=fnt, fill=(255,255,255,255))
    out = Image.alpha_composite(base, updated_image)
    out.save("final.png")

def embed_help():
    embeded = discord.Embed(
        title="YogiBot Commands",
        description= "Below are a list of yogibot commands. They must start with $"
    )
    embeded.add_field(name="yogi", value="This command sends a randomized text response.")
    embeded.add_field(name="photo", value="This command will prompt the user for a custom caption for a randomly chosen photo.")
    embeded.add_field(name="meme", value="This command sends a randomized GIF meme.")
    embeded.add_field(name="guess", value="Pick a number, any number between 1-20!")
    return embeded
   
client.run(ACCESS_TOKEN)