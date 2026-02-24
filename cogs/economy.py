import discord
from discord.ext import commands
import aiosqlite
from config import DB_NAME, START_BALANCE

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ensure_user(self, user_id):
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute("""
            INSERT OR IGNORE INTO users(user_id, wallet)
            VALUES (?, ?)
            """, (user_id, START_BALANCE))
            await db.commit()

    @commands.command()
    async def balance(self, ctx):
        await self.ensure_user(ctx.author.id)

        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute(
                "SELECT wallet FROM users WHERE user_id=?",
                (ctx.author.id,))
            wallet = (await cursor.fetchone())[0]

        embed = discord.Embed(
            title="💰 Balance",
            description=f"{wallet} coins",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
