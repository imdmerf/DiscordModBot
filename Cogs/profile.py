from discord.ext import commands
import discord
import sqlite3
from Main import *
from someimportantthings import TRUSTED_CHANNELS

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx):
        if ctx.channel.id in TRUSTED_CHANNELS:
            id = ctx.author.id
            stat = cursor.execute(f"SELECT status FROM users WHERE id = {id}").fetchone()[0]
            bal = cursor.execute(f"SELECT balance FROM users WHERE id = {id}").fetchone()[0]
            lov = cursor.execute(f"SELECT lover FROM users WHERE id = {id}").fetchone()[0]
            embed = discord.Embed(title=f"Профиль — {ctx.message.author}") # главный эмбед
            embed.add_field(name=">>> Статус: ", value=f"`{stat}`", inline=True)
            embed.set_thumbnail(url=ctx.author.avatar_url)  # ава справа квадратная
            embed.add_field(name=">>> Баланс: ", value=f"`{bal}`", inline=True)
        #   embed.add_field(name=">>> Голосовой онлайн: ", value="`0 ч / 0 м`", inline=True)
            embed.add_field(name=">>> Возлюбленный/ая: ", value=f"`{lov}`", inline=True)
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=embed)

    @commands.command()
    async def status(self, ctx, *, ys = None):
        if ctx.channel.id in TRUSTED_CHANNELS:
            author = ctx.author.id
            cursor.execute(f"UPDATE users SET status = '{ys}' WHERE id = '{author}'")
            connection.commit()
            await ctx.channel.purge(limit=1)

        
def setup(bot):
    bot.add_cog(mod(bot=bot))