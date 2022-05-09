import json
from datetime import datetime

import discord
from discord.ext import commands

from lib.Cache import servers
from lib.setting_menu import ServerThings

with open("config.json") as fp:
    data = json.load(fp)


class auto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counter = 0

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            if ctx.message.content == "t!help":
                await ctx.send("We are using / Commands now!")
        else:
            self.counter = + 1
            channel = self.bot.get_channel(data["error"])
            embed = discord.Embed(title="Ops, there is an error!",
                                  description="Error report Nr. {} after reset.".format(self.counter),
                                  color=ctx.author.color)
            embed.add_field(name='Server:', value='{}'.format(ctx.message.guild), inline=True)
            embed.add_field(name='Command:', value='{}'.format(ctx.message.content), inline=False)
            embed.add_field(name='Error:', value="```python\n{}```".format(error), inline=False)
            embed.set_thumbnail(url=self.bot.user.avatar)
            embed.set_footer(text='Error Message', icon_url=ctx.message.author.avatar)
            embed.timestamp = datetime.utcnow()
            await ctx.channel.send(embed=embed)
            await channel.send(embed=embed)
            print(error)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        channel = self.bot.get_channel(data["error"])
        embed = discord.Embed(title="Ops, there is an error!",
                              color=ctx.author.color)
        embed.add_field(name='Server:', value='{}'.format(ctx.guild), inline=True)
        embed.add_field(name='Command:', value='{}'.format(ctx.command.name), inline=False)
        embed.add_field(name='Error:', value="```python\n{}```".format(error), inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text='Error Message', icon_url=ctx.author.avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.respond(embed=embed)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        ServerThings(guild.id).create_server(guild.icon)
        servers.cache_clear()
        channel = self.bot.get_channel(data["server"])
        embed = discord.Embed(title="Server join")
        embed.add_field(name='Name:', value='{}'.format(guild.name), inline=True)
        embed.add_field(name='Server ID:', value='{}'.format(guild.id), inline=True)
        embed.timestamp = datetime.utcnow()
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        ServerThings(guild.id).delete_server()
        servers.cache_clear()
        channel = self.bot.get_channel(data["server"])
        embed = discord.Embed(title="Server leave", description="Timmy leaved *{0}*".format(guild.name),
                              color=discord.Color.blurple())
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(auto(bot))
