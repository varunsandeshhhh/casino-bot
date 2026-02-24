import discord
from discord.ext import commands
import asyncio
from database import init_db
import config

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def main():
    async with bot:
        await init_db()
        await bot.load_extension("cogs.economy")
        await bot.load_extension("cogs.blackjack")
        await bot.load_extension("cogs.tournament")
        await bot.start(config.TOKEN)

asyncio.run(main())
