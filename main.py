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


TITLE_RE = re.compile(r"^\[\[(.*?)\]\]$", re.DOTALL | re.IGNORECASE)

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    title = message.content

    try:
        result = await get_goodreads_book(title)
    except Exception as exc:
        await message.channel.send(f"Couldn't reach Goodreads: {exc}")
        return

    embed = create_embed(result)

    await message.channel.send(embed=embed)


async def get_goodreads_book(title: str) -> dict:

    # print("here")

    url = "https://goodreads12.p.rapidapi.com/searchBooks"
    params = {"keyword": title, "page": 1}
    headers = {
        "x-rapidapi-key": GOODREADS_API_KEY,
        "x-rapidapi-host": "goodreads12.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, params=params)

    print(response.json())

    return response.json()


def create_embed(book) -> discord.Embed:

    print("here")

    title = book.get('title')
    authors = [a.get('name', '') for a in book.get('author', [])]
    img = book.get("imageUrl")

    embed = discord.Embed(
        title=title,
        description=f"Author(s): {authors}",
        color=discord.Color.blurple()
    )
    if img:
        embed.set_thumbnail(url=img)
    return embed


bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)

