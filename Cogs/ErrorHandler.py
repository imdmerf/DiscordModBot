from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
import discord.utils

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        member=discord.Embed(title="Ошибка", description="Пользователь не найден. Проверьте правильность и повторите попытку!", color=0x000000)
        member.set_thumbnail(url="https://cdn.discordapp.com/attachments/665961371074297856/913362290848432148/NicePng_warning-symbol-png_1358116.png")
        arg=discord.Embed(title="Ошибка", description="Отсутствует аргумент!", color=0x000000)
        arg.set_thumbnail(url="https://cdn.discordapp.com/attachments/665961371074297856/913362290848432148/NicePng_warning-symbol-png_1358116.png")
        role=discord.Embed(title="Ошибка", description="Данная роль еще не задана!", color=0x000000)
        role.set_thumbnail(url="https://cdn.discordapp.com/attachments/665961371074297856/913362290848432148/NicePng_warning-symbol-png_1358116.png")
        perm=discord.Embed(title="Ошибка", description="Недостаточно прав!", color=0x000000)
        perm.set_thumbnail(url="https://cdn.discordapp.com/attachments/665961371074297856/913362290848432148/NicePng_warning-symbol-png_1358116.png")

        if isinstance(error, commands.CommandNotFound):
            None
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=member, delete_after=5)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=arg, delete_after=5)
        if isinstance(error, commands.MissingRole):
            await ctx.send(embed=role, delete_after=5)
        if isinstance(error, MissingPermissions):
            await ctx.send(embed=perm)


def setup(bot):
    bot.add_cog(ErrorHandler(bot=bot))