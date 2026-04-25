import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests
import aiohttp
import re
import json

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOODREADS_API_KEY = os.getenv('GOODREADS_API_KEY')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#
#     await bot.process_commands(message)

# !hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command()
async def embed(ctx):
    embed = discord.Embed(title="I am a Title", description="I am the description")
    await ctx.send(embed=embed)


TITLE_RE = re.compile(r"^\[\[(.*?)\]\]$", re.DOTALL | re.IGNORECASE)

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    title = message.content

    result = await get_openlibrary_book(title)

    embed = create_embed(result)

    await message.channel.send(embed=embed)


async def get_openlibrary_book(title: str):

    words = title.split()
    joined = "+".join(words)

    url = f"https://openlibrary.org/search.json?q={joined}"
    headers = {
        "User-Agent": "MyAppName/1.0 (myemail@example.com)"
    }
    response = requests.get(url, headers=headers)
    print(response.json()["docs"][0])
    return response.json()["docs"][0]


# async def get_goodreads_book(title: str) -> dict:
#
#     # print("here")
#
#     url = "https://goodreads12.p.rapidapi.com/searchBooks"
#     params = {"keyword": title, "page": 1}
#     headers = {
#         "x-rapidapi-key": GOODREADS_API_KEY,
#         "x-rapidapi-host": "goodreads12.p.rapidapi.com",
#         "Content-Type": "application/json"
#     }
#
#     response = requests.get(url, headers=headers, params=params)
#
#     book = response.json()[0]
#     print(book)
#
#     print(response.json())
#
#     return response.json()


def create_embed(book) -> discord.Embed:

    title = book["title"]
    author = book["author_name"]
    year = book["first_publish_year"]

    embed = discord.Embed(
        title=title,
        description=f"Author: {author}",
        color=discord.Color.blurple()
    )
    return embed


bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)

