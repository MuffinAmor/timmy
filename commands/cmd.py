from datetime import datetime

import discord
from discord import slash_command
from discord.ext import commands

from interactiv.SetupModal import MyModal
from lib.Cache import config, servers


class CommandClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="support", description="An Invitelink for our Support Server!")
    async def support(self, ctx):
        if not ctx.author.bot:
            channel = self.bot.get_channel(754413698616918091)
            invitelinknew = await channel.create_invite(max_age=600, reason="Support")
            embed = discord.Embed(color=ctx.author.color)
            embed.add_field(name="Support Server Invite Link",
                            value="[Do you need help? Click me!]({})".format(invitelinknew))
            embed.timestamp = datetime.utcnow()
            await ctx.respond(embed=embed)

    @slash_command(name="help", description="Open the Help Menu")
    async def help(self, ctx):
        if not ctx.author.bot:
            embed = discord.Embed(title="Help Menu", color=discord.Color(config()["color"]))
            embed.add_field(name="/set_desc", value="Set your description!",
                            inline=False)
            embed.add_field(name="/set_channel", value="Set an advertising Channel!",
                            inline=False)
            embed.add_field(name="/bump", value="Bump your Server!",
                            inline=False)
            embed.add_field(name="/botinfo", value="Some neat infos about Timmy",
                            inline=False)
            embed.add_field(name="/invite", value="Do you ant to invite the Bot to your Server?",
                            inline=False)
            embed.add_field(name="/support", value="Meet us on our Support Server!",
                            inline=False)
            embed.set_footer(text="This is supposed to be something!", icon_url=ctx.author.avatar)
            embed.set_thumbnail(url=ctx.guild.icon)
            embed.timestamp = datetime.utcnow()
            await ctx.respond(embed=embed)

    @slash_command(name="botinfo", description="Infos about Timmy")
    async def botinfo(self, ctx):
        l = list(permi for permi, value in ctx.guild.me.guild_permissions if str(value) == 'True')
        i = '\n📍 '.join(l)
        if "administrator" in i:
            i = "administrator"
        embed = discord.Embed(title="{}'s info".format(self.bot.user.name), color=discord.Color(config()["color"]))
        embed.add_field(name="Name", value=self.bot.user, inline=True)
        embed.add_field(name="Server", value=len(self.bot.guilds))
        embed.add_field(name='Bot Permissions', value='📍 {0}'.format(i), inline=False)
        embed.set_footer(text="System: Timmy | Maintained by: muffinamor.dev", icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        await ctx.respond(embed=embed)

    @slash_command(name="invite", description="Create an invite link!")
    async def invite(self, ctx):
        permissions = discord.Permissions(51297)
        dinge = discord.utils.oauth_url(self.bot.user.id, permissions=permissions,
                                        scopes=("bot", "applications.commands"),
                                        disable_guild_select=False)
        embed = discord.Embed(title=f"Here is the invite for: {self.bot.user.name}",
                              description=f"[Click me!]({dinge})", color=discord.Color(config()["color"]))
        await ctx.respond(embed=embed)

    @commands.has_guild_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    @slash_command(name="set_desc", description="Descripe your Server!")
    async def set_desc(self, ctx):
        modal = MyModal(ctx.guild)
        servers.cache_clear()
        await ctx.interaction.response.send_modal(modal)


def setup(bot):
    bot.add_cog(CommandClass(bot))
