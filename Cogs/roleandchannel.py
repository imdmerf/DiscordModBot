from typing import Text
from discord import embeds, guild, widget
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.core import command
import discord.utils
from Main import *
import datetime
from someimportantthings import VERIFY_ROLE, CHANNEL_FOR_LOGS, SERVER_ID
intents.members = True

class rolechannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, id=VERIFY_ROLE) # Сюда ввести верификационную роль
        ch = bot.get_channel(CHANNEL_FOR_LOGS) # id канала, куда нужно высылать лог
        startembed = discord.Embed(title=f"Новый участник на сервере", color=0x32353b)
        startembed.add_field(name=f">>> Ник:", value=member.mention, inline=True)
        startembed.add_field(name=f">>> Дата регистрации", value=f"`{member.created_at}`", inline=False)
        startembed.set_thumbnail(url=member.avatar_url)
        startembed.timestamp = datetime.datetime.utcnow()
        for guild in bot.guilds:
            for member in guild.members:
                if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                    cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 'Не задан', 'Ещё нет', 'Ещё нет', 'Отсутствует', 0, 0, 0)")
                else:
                    pass
                connection.commit()

        await member.add_roles(role)
        await ch.send(embed=startembed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        ch = bot.get_channel(CHANNEL_FOR_LOGS) # id канала, куда нужно высылать лог
        startembed = discord.Embed(title=f"Участник покинул сервер", color=0x32353b)
        startembed.add_field(name=f">>> Ник:", value=member.mention, inline=True)
        startembed.add_field(name=f">>> Дата регистрации", value=f"`{member.created_at}`", inline=False)
        startembed.set_thumbnail(url=member.avatar_url)
        startembed.timestamp = datetime.datetime.utcnow()
        await ch.send(embed=startembed)


    @commands.group(name ="role", invoke_without_command=True, pass_context=True)
    async def role(self, ctx, *args):
        pass
    
    @role.command(pass_context=True)
    async def create(self, ctx, rolename = None):
        author = ctx.message.author
        perms = discord.Permissions(0)
        id = ctx.author.id
        guild = self.bot.get_guild(SERVER_ID)
        rc = cursor.execute(f"SELECT rolecounter FROM users WHERE id = '{id}'").fetchone()[0]
        connection.commit()
        errembed = discord.Embed(title=f"Вы не можете создать еще одну личную роль", color=0x32353b)   
        ch = bot.get_channel(CHANNEL_FOR_LOGS) # id канала, куда нужно высылать лог
        embed = discord.Embed(title=f"Пользователь создал личную роль", color=0x32353b, timestamp=ctx.message.created_at)
        embed.add_field(name=f">>> Пользователь:", value=author.mention, inline=True)
        embed.add_field(name=f">>> Название личной роли", value=f"`{rolename}`", inline=True)
        embed.set_thumbnail(url=author.avatar_url)
        if rc >= 1:
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=errembed, delete_after=5)
        else:
            await guild.create_role(name=rolename, permissions=perms)
            role = discord.utils.get(author.guild.roles, name=rolename)
            cursor.execute(f"UPDATE users SET rolecounter = rolecounter + 1 WHERE id = '{id}'")
            connection.commit()
            cursor.execute(f"UPDATE users SET roleid = '{role.id}' WHERE id = '{id}'")
            connection.commit()
            cursor.execute(f"UPDATE users SET rolename = '{rolename}' WHERE id = '{id}'")
            connection.commit()
            await author.add_roles(role)
            await ctx.channel.purge(limit=1)
            await ch.send(embed=embed)

    @role.command(pass_context=True)
    async def manage(self, ctx):
        author = ctx.message.author
        ch = bot.get_channel(CHANNEL_FOR_LOGS) # id канала, куда нужно высылать лог
        id = ctx.author.id
        rolename = cursor.execute(f"SELECT rolename FROM users WHERE id = '{id}'").fetchone()[0]
        errem = discord.Embed(title=f"Пользователь — `{author}`", color=0x32353b)
        errem.set_author(name="Меню управления личной ролью")
        errem.add_field(name=">>> Вы еще не обладаете лично ролью, но можете её создать", value="\u200b", inline=True)
        errem.set_thumbnail(url=author.avatar_url)
        delembed = discord.Embed(title=f"Пользователь удалил личную роль", color=0x32353b, timestamp=ctx.message.created_at)
        delembed.add_field(name=f">>> Пользователь:", value=author.mention, inline=True)
        delembed.add_field(name=f">>> Название личной роли", value=f"`{rolename}`", inline=True)
        delembed.set_thumbnail(url=author.avatar_url)
        dbid  = cursor.execute(f"SELECT roleid FROM users WHERE id = '{id}'").fetchone()[0]
        if dbid == 0:
            await ctx.send(embed=errem)
        roleid = discord.utils.get(author.guild.roles, id=dbid)
        startembed = discord.Embed(title=f"Пользователь — `{author}`", color=0x32353b)
        startembed.set_author(name="Меню управления личной ролью")
        startembed.add_field(name=">>> Личная роль:", value=roleid.mention, inline=True)
        startembed.set_thumbnail(url=author.avatar_url)
        guild = self.bot.get_guild(SERVER_ID)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=startembed, 
                components=[
                [Button(style=ButtonStyle.gray, label="Изменить цвет", emoji="🎨"),
                Button(style=ButtonStyle.red, label="Удалить роль", emoji="🗑️"),],
                [Button(style=ButtonStyle.red, label="Отмена", emoji="❌")]
            ],
        )

        response = await bot.wait_for("button_click")
        if response.channel == ctx.channel:
            if response.component.label == "Изменить цвет":
                await ctx.channel.purge(limit=2)
                colorembed = discord.Embed(title=f"Пользователь — `{author}`", color=0x32353b)
                colorembed.set_author(name="Изменение цвета личной роли")
                colorembed.add_field(name=">>> Личная роль:", value=roleid.mention, inline=True)
                colorembed.set_thumbnail(url=author.avatar_url)
                await ctx.send(embed=colorembed, 
                        components=[
                        [Button(style=ButtonStyle.gray, label="Красный", emoji="🔴"),
                        Button(style=ButtonStyle.gray, label="Оранжевый", emoji="🟠"),
                        Button(style=ButtonStyle.gray, label="Желтый", emoji="🟡"),
                        Button(style=ButtonStyle.gray, label="Зеленый", emoji="🟢"),],
                        [Button(style=ButtonStyle.gray, label="Синий", emoji="🔵"),
                        Button(style=ButtonStyle.gray, label="Лиловый", emoji="🟣"),
                        Button(style=ButtonStyle.gray, label="Черный", emoji="⚫"),
                        Button(style=ButtonStyle.gray, label="Белый", emoji="⚪"),],
                        [Button(style=ButtonStyle.red, label="Отмена", emoji="❌")]
                    ],
                )

                response = await bot.wait_for("button_click")
                if response.channel == ctx.channel:
                    if response.component.label == "Красный":   
                        await roleid.edit(colour = 0xff0000)
                        await ctx.channel.purge(limit=1)

                    elif response.component.label == "Оранжевый":   
                        await roleid.edit(colour = 0xff6800)
                        await ctx.channel.purge(limit=1)

                    elif response.component.label == "Желтый":   
                        await roleid.edit(colour = 0xffff00)
                        await ctx.channel.purge(limit=1)

                    elif response.component.label == "Зеленый":   
                        await roleid.edit(colour = 0x008000)
                        await ctx.channel.purge(limit=1)

                    elif response.component.label == "Синий":   
                        await roleid.edit(colour = 0x0000ff)
                        await ctx.channel.purge(limit=1)

                    elif response.component.label == "Лиловый":   
                        await roleid.edit(colour = 0x9932cc)
                        await ctx.channel.purge(limit=1)

                    elif response.component.label == "Черный":   
                        await roleid.edit(colour = 0x080101)
                        await ctx.channel.purge(limit=1)

                    elif response.component.label == "Белый":   
                        await roleid.edit(colour = 0xffffff)
                        await ctx.channel.purge(limit=1)
                    
                    elif response.component.label == "Отмена":   
                        pass
                        await ctx.channel.purge(limit=1)

            elif response.component.label == "Удалить роль":
                accembed = discord.Embed(title=f"Вы уверены?", color=0x32353b)
                accembed.add_field(name="`Данное действие необратимо`", value="\u200b", inline=True)
                await ctx.channel.purge(limit=1)
                await ctx.send(embed=accembed, 
                        components=[
                        [Button(style=ButtonStyle.green, label="Да", emoji="✅"),
                        Button(style=ButtonStyle.red, label="Нет", emoji="❌"),],
                    ],
                )

                response = await bot.wait_for("button_click")
                if response.channel == ctx.channel:
                    if response.component.label == "Да":
                            await roleid.delete()
                            cursor.execute(f"UPDATE users SET rolecounter = 0 WHERE id = '{id}'")
                            connection.commit()
                            cursor.execute(f"UPDATE users SET roleid = 0 WHERE id = '{id}'")
                            connection.commit()
                            cursor.execute(f"UPDATE users SET rolename = 'Отсутствует' WHERE id = '{id}'")
                            connection.commit()
                            pass
                            await ctx.channel.purge(limit=1)
                            await ch.send(embed=delembed)
                    
                    elif response.component.label == "Нет":
                        pass
                        await ctx.channel.purge(limit=1)

            elif response.component.label == "Отмена":
                pass
                await ctx.channel.purge(limit=1)        



def setup(bot):
    bot.add_cog(rolechannel(bot=bot))