from sqlite3.dbapi2 import Cursor
import discord
from discord import client
from discord.flags import Intents
from Config import Token, OWNERID 
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
import os
from discord import utils
import sqlite3

connection = sqlite3.connect ("./Cogs/members.db", timeout=10)
cursor = connection.cursor()

intents = discord.Intents.all()

intents.members = True

bot = discord.Client()
bot = commands.Bot(command_prefix="!", case_insensitive=True, guild_subscriptions=True, intents = intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    DiscordComponents(bot)
    print('Bot online: {0.user}'.format(bot))  # состояние бота
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT,
        balance BIGINT,
        status TEXT,
        lover TEXT,
        loverid INT,
        rolename TEXT,
        roleid INT,
        rolecounter INT,
        onvoicetime INT
    )""")
    connection.commit()

    for guild in bot.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 'Не задан', 'Ещё нет', 'Ещё нет', 'Отсутствует', 0, 0, 0)")
            else:
                pass
            connection.commit()



for filename in os.listdir('./Cogs'):  # подгружаем все .py файлы из папки 'Cogs'
    if filename.endswith('.py'):
        bot.load_extension(f"Cogs.{filename[:-3]}")


@bot.command()
async def load(ctx, extension):  # прописываем команду подгрузки когов
    if ctx.author.id == OWNERID:
        bot.load_extension(f"Cogs.{extension}")
        await ctx.channel.purge(limit=1)
        await ctx.send("Cog is loaded")
    else:
        await ctx.channel.purge(limit=1)
        await ctx.send("Access denied")  # в случаи несовпадения айди запрещает доступ


@bot.command()
async def unload(ctx, extension):  # прописываем команду выгрузки когов
    if ctx.author.id == OWNERID:
        bot.unload_extension(f"Cogs.{extension}")
        await ctx.channel.purge(limit=1)
        await ctx.send("Cog is unloaded")
    else:
        await ctx.channel.purge(limit=1)
        await ctx.send("Access denied")  # в случаи несовпадения айди запрещает доступ


@bot.command()
async def reload(ctx, extension):  # прописываем команду перезагрузки когов
    if ctx.author.id == OWNERID:
        bot.reload_extension(f"Cogs.{extension}")
        await ctx.channel.purge(limit=1)
        await ctx.send("Cog is reloaded")
    else:
        await ctx.channel.purge(limit=1)
        await ctx.send("Access denied")  # в случаи несовпадения айди запрещает доступ


bot.run(Token)
