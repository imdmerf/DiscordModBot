from sqlite3.dbapi2 import Timestamp
from typing import Text
from discord import embeds, guild, widget
from discord.ext import commands
from discord.ext.commands.core import command
import discord.utils
from Main import *
import datetime
import re
import asyncio
from someimportantthings import GIRLS_ROLE, BOYS_ROLE, TRUSTED_CHANNELS, CHANNEL_FOR_LOGS, MUTE_ROLE


time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

intents = discord.Intents.default()

intents.members = True

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} Некоректный ключ времени!".format(k))
            except ValueError:
                raise commands.BadArgument("{} Это не число!".format(v))
        return time

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member, *, reason="Не задана"):
        if ctx.channel.id in TRUSTED_CHANNELS:
            ch = bot.get_channel(CHANNEL_FOR_LOGS) # id канала, куда нужно высылать лог
            author = ctx.message.author
            image = author.avatar_url
            for_user=discord.Embed(title=f"Здравствуй, {member}", description=f"", color=0x32353b)
            for_user.add_field(name=">>> Причина бана", value=f"`{reason}`", inline=True)
            for_user.set_footer(text=f"Бан выдал: {author}", icon_url=image)
            for_user.set_thumbnail(url=member.avatar_url)
            embed = discord.Embed(title=f"ЛОГ - Бан", color=0x32353b, timestamp=ctx.message.created_at)
            embed.add_field(name=f">>> Пользователь:", value=member.mention, inline=True)
            embed.add_field(name=f">>> Причина бана:", value=f"`{reason}`", inline=True)
            embed.set_footer(text=f"Бан выдал: {author}", icon_url=image) 
            embed.set_thumbnail(url=member.avatar_url)
            try:
                await member.send(embed=for_user)
            except: 
                await ctx.send("Личка пользователя закрыта!")
            await member.ban(reason=reason)
            await ch.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member, *, reason="Не задана"):
        if ctx.channel.id in TRUSTED_CHANNELS:
            ch = bot.get_channel(CHANNEL_FOR_LOGS) # id канала, куда нужно высылать лог
            author = ctx.message.author
            image = author.avatar_url
            for_user=discord.Embed(title=f"Здравствуй, {member}", description=f"", color=0x32353b)
            for_user.add_field(name=">>> Причина кика", value=f"`{reason}`", inline=True)
            for_user.set_footer(text=f"Кикнул: {author}", icon_url=image)
            for_user.set_thumbnail(url=member.avatar_url)
            embed = discord.Embed(title=f"ЛОГ - Кик", color=0x32353b, timestamp=ctx.message.created_at)
            embed.add_field(name=f">>> Пользователь:", value=member.mention, inline=True)
            embed.add_field(name=f">>> Причина кика:", value=f"`{reason}`", inline=True)
            embed.set_footer(text=f"Кик выдал: {author}", icon_url=image) 
            embed.set_thumbnail(url=member.avatar_url)
            await member.kick(reason=reason)
            try:
                await member.send(embed=for_user)
            except:
                await ctx.send("Личка пользователя закрыта!", delete_after=5)
            await ch.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_messages=True, manage_roles=True)
    async def mute(self, ctx, member:discord.Member,  time:TimeConverter = None, *, reason="Не задана"):
        if ctx.channel.id in TRUSTED_CHANNELS:
            author = ctx.message.author
            image = author.avatar_url
            ch = bot.get_channel(CHANNEL_FOR_LOGS) # id канала, куда нужно высылать лог
            role = discord.utils.get(member.guild.roles, id=MUTE_ROLE) # Роль для мута
            startembed = discord.Embed(title=f"Нарушитель — `{member}`", color=0x32353b)
            startembed.set_author(name="Меню выдачи мута")
            startembed.add_field(name=">>> Причина мута", value=f"`{reason}`", inline=True)
            startembed.add_field(name=">>>  Срок мута", value=f"`{time/60} минут`", inline=True)
            startembed.set_footer(text=f"Мут выдаёт: {author}", icon_url=image) 
            startembed.set_thumbnail(url=member.avatar_url)
            for_usertext=discord.Embed(title=f"Здравствуй, {member}", description=f"Ты получил мут текстового чата на: {time/60} минут", color=0x32353b)
            for_usertext.set_footer(text=f"Выдал мут: {author}", icon_url=image)
            for_usertext.add_field(name=">>> Причина мута", value=f"`{reason}`", inline=True)
            for_usertext.set_thumbnail(url=member.avatar_url)
            for_uservoice=discord.Embed(title=f"Здравствуй, {member}", description=f"Ты получил мут голосового чата на: {time/60} минут", color=0x32353b)
            for_uservoice.set_footer(text=f"Выдал мут: {author}", icon_url=image)
            for_uservoice.add_field(name=">>> Причина мута", value=f"`{reason}`", inline=True)
            for_uservoice.set_thumbnail(url=member.avatar_url)
            for_usercandv=discord.Embed(title=f"Здравствуй, {member}", description=f"Ты получил мут текстового и голосового чата на: {time/60} минут", color=0x32353b)
            for_usercandv.set_footer(text=f"Выдал мут: {author}", icon_url=image)
            for_usercandv.add_field(name=">>> Причина мута", value=f"`{reason}`", inline=True)
            for_usercandv.set_thumbnail(url=member.avatar_url)
            tembed = discord.Embed(title=f"ЛОГ - выдача мута", color=0x32353b, timestamp=ctx.message.created_at)
            tembed.add_field(name=f">>> Пользователь:", value=member.mention, inline=True)
            tembed.add_field(name=f">>> Причина мута:", value=f"`{reason}`", inline=True)
            tembed.add_field(name=f">>> Вид мута:", value="`Текстовый`", inline=False)
            tembed.add_field(name=f">>> Срок мута в минутах:", value=f"`{time/60}`", inline=True)
            tembed.set_footer(text=f"Мут выдал: {author}", icon_url=image) 
            tembed.set_thumbnail(url=member.avatar_url)
            vembed = discord.Embed(title=f"ЛОГ - выдача мута", color=0x32353b, timestamp=ctx.message.created_at)
            vembed.add_field(name=f">>> Пользователь:", value=member.mention, inline=True)
            vembed.add_field(name=f">>> Причина мута:", value=f"`{reason}`", inline=True)
            vembed.add_field(name=f">>> Вид мута:", value="`Голосовой`", inline=False)
            vembed.add_field(name=f">>> Срок мута в минутах:", value=f"`{time/60}`", inline=True)
            vembed.set_footer(text=f"Мут выдал: {author}", icon_url=image) 
            vembed.set_thumbnail(url=member.avatar_url)
            tvembed = discord.Embed(title=f"ЛОГ - выдача мута", color=0x32353b, timestamp=ctx.message.created_at)
            tvembed.add_field(name=f">>> Пользователь:", value=member.mention, inline=True)
            tvembed.add_field(name=f">>> Причина мута:", value=f"`{reason}`", inline=True)
            tvembed.add_field(name=f">>> Вид мута:", value="`Текстовый и голосовой`", inline=False)
            tvembed.add_field(name=f">>> Срок мута в минутах:", value=f"`{time/60}`", inline=True)
            tvembed.set_footer(text=f"Мут выдал: {author}", icon_url=image) 
            tvembed.set_thumbnail(url=member.avatar_url)
            err=discord.Embed(title=f"{member} не находится на голосовом канале", color=0x32353b)
            err.set_author(name="Действие невозможно")
            role_err=discord.Embed(title=f"{member} уже получил мут", color=0x32353b)
            role_err.set_author(name="Действие невозможно")
            await ctx.send(embed=startembed, 
                    components=[
                    [Button(style=ButtonStyle.grey, label="Только чат", emoji="💬"),
                    Button(style=ButtonStyle.grey, label="Только войс", emoji="🎤"),
                    Button(style=ButtonStyle.grey, label="Чат и войс", emoji="🔇")],
                    [Button(style=ButtonStyle.red, label="Отмена", emoji="❌"),]
                ],
            )

            response = await bot.wait_for("button_click")
            if response.channel == ctx.channel:
                if response.component.label == "Только чат":
                    if role in member.roles:
                        await ctx.channel.purge(limit=2)
                        await ctx.send(embed=role_err, delete_after=5)
                    else:
                        try:
                            await member.send(embed=for_usertext)
                        except:
                            await ctx.send("Личка пользователя закрыта!", delete_after=5)
                        await ctx.channel.purge(limit=2)
                        await ch.send(embed=tembed)
                        await member.add_roles(role)
                        if time:
                            await asyncio.sleep(time)
                            await member.remove_roles(role)

                elif response.component.label == "Только войс":
                    if member.voice is not None:
                            try:
                                await member.send(embed=for_uservoice)
                            except:
                                await ctx.send("Личка пользователя закрыта!", delete_after=5)
                            await ctx.channel.purge(limit=2)
                            await ch.send(embed=vembed)
                            await member.edit(mute=True)
                            if time:
                                await asyncio.sleep(time)
                                await member.edit(mute=False)
                    else:
                        await ctx.channel.purge(limit=2)
                        await ctx.send(embed=err, delete_after=5)

                elif response.component.label == "Чат и войс":
                    if member.voice is not None:
                        if role in member.roles:
                            await ctx.send(embed=role_err)
                        else:    
                            try:
                                await member.send(embed=for_usercandv)
                            except:
                                await ctx.send("Личка пользователя закрыта!", delete_after=5)
                            await ctx.channel.purge(limit=2)
                            await ch.send(embed=tvembed)
                            await member.add_roles(role)
                            await member.edit(mute=True)
                            if time:
                                await asyncio.sleep(time)
                                await member.edit(mute=False)
                                await member.remove_roles(role)
                    else:
                        await ctx.channel.purge(limit=2)
                        await ctx.send(embed=err, delete_after=5)
                
                elif response.component.label == "Отмена":
                    await ctx.channel.purge(limit=2)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def gender(self, ctx, member:discord.Member):
        if ctx.channel.id in TRUSTED_CHANNELS:
            ch = bot.get_channel(CHANNEL_FOR_LOGS) # id канала, куда нужно высылать лог
            author = ctx.message.author
            image = author.avatar_url
            startembed = discord.Embed(title=f"Меню выдачи гендерной роли", color=0x32353b)
            startembed.add_field(name=f">>> Пользователь — `{member}`", value="\u200b", inline=True)
            startembed.set_footer(text=f"Роль выдаёт: {author}", icon_url=image) 
            startembed.set_thumbnail(url=member.avatar_url)
            role = discord.utils.get(member.guild.roles, id=GIRLS_ROLE) # Роль для девочки
            secondrole= discord.utils.get(member.guild.roles, id=BOYS_ROLE)  # Роль для мальчика
            fembed = discord.Embed(title=f"ЛОГ - выдача гендерной роли", color=0x32353b, timestamp=ctx.message.created_at)
            fembed.add_field(name=f">>> Пользователь:", value=member.mention, inline=True)
            fembed.add_field(name=f">>> Выданная роль:", value=role.mention, inline=True)
            fembed.set_footer(text=f"Роль выдал: {author}", icon_url=image) 
            fembed.set_thumbnail(url=member.avatar_url)
            membed = discord.Embed(title=f"ЛОГ - выдача гендерной роли", color=0x32353b, timestamp=ctx.message.created_at)
            membed.add_field(name=f">>> Пользователь:", value=member.mention, inline=True)
            membed.add_field(name=f">>> Выданная роль:", value=secondrole.mention, inline=True)
            membed.set_footer(text=f"Роль выдал: {author}", icon_url=image) 
            membed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=startembed, 
                    components=[
                    [Button(style=ButtonStyle.gray, label="Парень", emoji="♂️"),
                    Button(style=ButtonStyle.gray, label="Девушка", emoji="♀️"),],
                    [Button(style=ButtonStyle.red, label="Отмена", emoji="❌"),]
                ],
            )

            response = await bot.wait_for("button_click")
            if response.channel == ctx.channel:
                if response.component.label == "Парень":
                    await ctx.channel.purge(limit=2)
                    await member.remove_roles(role)
                    await member.add_roles(secondrole)
                    await ch.send(embed=membed)

                elif response.component.label == "Девушка":
                    await ctx.channel.purge(limit=2)
                    await member.remove_roles(secondrole)
                    await member.add_roles(role)
                    await ch.send(embed=fembed)

                elif response.component.label == "Отмена":
                    await ctx.channel.purge(limit=2)       

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def swap(self, ctx, member:discord.Member):
        if ctx.channel.id in TRUSTED_CHANNELS:
            ch = bot.get_channel(CHANNEL_FOR_LOGS)
            success=discord.Embed(title=f'\u200b',description=f'Роль для {member} обновлена', color=0x32353b)
            success.set_thumbnail(url=member.avatar_url)
            fr = discord.utils.get(member.guild.roles, id=BOYS_ROLE) # Роль для мальчика
            secondrole = discord.utils.get(member.guild.roles, id=GIRLS_ROLE) # Роль для девочки
            if fr in member.roles:
                await member.remove_roles(fr)
                await member.add_roles(secondrole)
            else:
                await member.remove_roles(secondrole)   
                await member.add_roles(fr)
                await ctx.channel.purge(limit=1)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def give(self,ctx, member:discord.Member, *, role: discord.Role):
        if ctx.channel.id in TRUSTED_CHANNELS:
            ch = bot.get_channel(CHANNEL_FOR_LOGS) # id канала, куда нужно высылать лог
            author = ctx.message.author
            image = author.avatar_url
            startembed = discord.Embed(title=f"ЛОГ - выдача роли", color=0x32353b, timestamp=ctx.message.created_at)
            startembed.add_field(name=f">>> Пользователь:", value=member.mention, inline=True)
            startembed.add_field(name=f">>> Выданная роль:", value=role.mention, inline=True)
            startembed.set_footer(text=f"Роль выдал: {author}", icon_url=image) 
            startembed.set_thumbnail(url=member.avatar_url)
            await member.add_roles(role)
            await ch.send(embed=startembed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def take(self,ctx, member:discord.Member, *, role: discord.Role):
        if ctx.channel.id in TRUSTED_CHANNELS:
            ch = bot.get_channel(CHANNEL_FOR_LOGS) # id канала, куда нужно высылать лог
            author = ctx.message.author
            image = author.avatar_url
            startembed = discord.Embed(title=f"ЛОГ - снятие роли", color=0x32353b, timestamp=ctx.message.created_at)
            startembed.add_field(name=f">>> Пользователь:", value=member.mention, inline=True)
            startembed.add_field(name=f">>> Cнятая роль:", value=role.mention, inline=True)
            startembed.set_footer(text=f"Роль снял: {author}", icon_url=image) 
            startembed.set_thumbnail(url=member.avatar_url)
            if role in member.roles:
                await member.remove_roles(role)
                await ch.send(embed=startembed)
            else:
                return

    @commands.command()
    async def clear(self, ctx, amount: int):  # задаем функцию, т.е. название команды.
        messages = await ctx.channel.purge(limit=amount + 1)  # пурджим сообщения, +1 т.к. наше тоже удалится

        
def setup(bot):
    bot.add_cog(mod(bot=bot))
