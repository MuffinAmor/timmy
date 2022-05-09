from discord import slash_command
from discord.ext import commands

from lib.setting_menu import ServerThings


class SupportClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @slash_command(name="del_server", description="Wipes a Server Description", guilds=[754413698277441566])
    async def del_server(self, ctx, guild_id):
        if not ctx.author.bot:
            response = ServerThings(guild_id).delete_server()
            if response:
                await ctx.respond("Der Server wurde erfolgreich aus der Datenbank entfernt.")
            else:
                await ctx.respond("Der angegebene Server wurde leider nicht gefunden.")


def setup(bot):
    bot.add_cog(SupportClass(bot))
