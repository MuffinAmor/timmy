import discord
from discord import slash_command
from discord.ext import commands

from lib.Cache import channels, servers, config, SomeFreeSpace
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
            servers.cache_clear()
            await ctx.respond(f"The advertising channel was set to {channel}")

    @slash_command(name="bump", description="Bump your server")
    async def bump(self, ctx):
        if not ctx.author.bot:
            respond = BumpStuff(ctx.guild.id).bump()
            if respond == "c":
                await ctx.respond("Please provide a description, before you bump your server!")
            elif respond == "d":
                await ctx.respond("It looks like, you do not have finish the setup.")
            elif SomeFreeSpace(str(ctx.guild.id)).get_invite() == "":
                await ctx.respond("Provide a invite before you bump your server.")
            elif servers()[ctx.guild.id]["channel_id"] == "":
                await ctx.respond("Don't you want to set an advertisement channel before you bump your server?")
            elif not self.bot.get_channel(int(servers()[ctx.guild.id]["channel_id"])):
                ChannelThings(ctx.guild.id).reset_channel()
                channels.cache_clear()
                await ctx.respond(
                    "At least, you need to have a advertisement channel that actually exist on this Server.\n"
                    "Or maybe i do not have even access to the channel."
                )
            else:
                channel = self.bot.get_channel(servers()[ctx.guild.id]["channel_id"])
                server_members = len(ctx.guild.members)
                channel_viewers = len(channel.members)
                if (channel_viewers / server_members) * 100 > 50:
                    await ctx.respond(
                        "Well at least, give >50% of your members reading access to the advertisement channel")
                elif respond == "b":
                    time = time_calc(JsonHandling(str(ctx.guild.id)).get_time(), 31600)
                    await ctx.respond(f"Sorry, you still need to wait {time}")
                else:
                    await self.sending_stuff(ctx.guild)
                    JsonHandling(str(ctx.guild.id)).edit_time()
                    await ctx.respond("Your Server has been bumped successfully!")

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
                embed.set_footer(text=f"Server Bump | {server.id}")
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
