import discord
from discord.ext import commands
import random
import aiosqlite
from config import *

def draw_card():
    return random.randint(1, 11)

def total(hand):
    return sum(hand)

class BlackjackView(discord.ui.View):
    def __init__(self, ctx, bet, vip=False):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.bet = bet
        self.vip = vip
        self.player = [draw_card(), draw_card()]
        self.dealer = [draw_card(), draw_card()]

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    async def end_game(self, interaction):
        player_total = total(self.player)
        dealer_total = total(self.dealer)

        while dealer_total < 17:
            self.dealer.append(draw_card())
            dealer_total = total(self.dealer)

        win = dealer_total > 21 or player_total > dealer_total
        payout = int(self.bet * (1.6 if self.vip else 1.5)) if win else -self.bet

        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute("""
            UPDATE users
            SET wallet = wallet + ?, 
                weekly_profit = weekly_profit + ?, 
                total_wager = total_wager + ?
            WHERE user_id=?
            """, (payout, payout, self.bet, self.ctx.author.id))
            await db.commit()

        result = "You Win!" if win else "You Lose!"
        await interaction.response.edit_message(
            content=f"{result}\nYour: {player_total} | Dealer: {dealer_total}",
            view=None
        )

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.primary)
    async def hit(self, interaction, button):
        self.player.append(draw_card())
        if total(self.player) > 21:
            await self.end_game(interaction)
        else:
            await interaction.response.edit_message(
                content=f"Your cards: {self.player}",
                view=self
            )

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.success)
    async def stand(self, interaction, button):
        await self.end_game(interaction)

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def blackjack(self, ctx, bet: int):
        view = BlackjackView(ctx, bet)
        await ctx.send("🃏 Blackjack", view=view)

async def setup(bot):
    await bot.add_cog(Blackjack(bot))
