import discord
from discord import slash_command
from discord.ext import commands

from lib.Cache import channels, servers, config
from lib.JsonThings import JsonHandling
from lib.func import time_calc
from lib.setting_menu import ChannelThings, BumpStuff


class PartnerClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    '''@slash_command(name="set_partner_channel", description="Set the MDH Partner Channel")
    @commands.has_permissions(manage_channels=True)
    async def set_partner_channel(self, ctx, channel:discord.TextChannel):
        if not ctx.author.bot:
            pass'''

    @slash_command(name="set_channel", description="Set your advertising channel!")
    @commands.has_permissions(manage_channels=True)
    async def set_channel(self, ctx, channel: discord.TextChannel):
        if not ctx.author.bot:
            ChannelThings(ctx.guild.id).set_channel(channel.id)
            channels.cache_clear()
            await ctx.respond(f"The advertising channel was set to {channel}")

    @slash_command(name="bump", description="Bump your server")
    async def bump(self, ctx):
        if not ctx.author.bot:
            respond = BumpStuff(ctx.guild.id).bump()
            if respond == "a":
                await self.sending_stuff(ctx.guild)
                JsonHandling(str(ctx.guild.id)).edit_time()
                await ctx.respond("Your Server has been bumped successfully!")
            elif respond == "b":
                time = time_calc(JsonHandling(str(ctx.guild.id)).get_time(), 31600)
                await ctx.respond(f"Sorry, you still need to wait {time}")
            elif respond == "c":
                await ctx.respond("Please provide a description, before you bump your server!")
            else:
                await ctx.respond("It looks like, you do not have finish the setup.")

    async def sending_stuff(self, server):
        channel_list = channels()
        server_things = servers()[server.id]
        print(channel_list)
        for i in channel_list:
            channel = self.bot.get_channel(int(i))
            if channel:
                embed = discord.Embed(title="Server Bump!",
                                      color=discord.Color(config()["color"]))
                embed.add_field(
                    name=server.name,
                    value=f"{server_things['description']}\n\n"
                          f"**Invite:**\n{server_things['server_invite']}\n")
                embed.set_footer(text="Server Bump")
                if server_things['img_url']:
                    embed.set_thumbnail(url=server_things['img_url'])
                try:
                    await channel.send(embed=embed)
                except Exception as e:
                    ChannelThings(server.id).delete_specific_channel(i)
            else:
                ChannelThings(server.id).delete_specific_channel(i)
                channels.cache_clear()


def setup(bot):
    bot.add_cog(PartnerClass(bot))
