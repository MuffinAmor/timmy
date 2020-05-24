from datetime import datetime

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='t!')

botcolor = 0x000ffc

bot.remove_command('help')


class cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command()
    async def help(self, ctx):
        if ctx.author.bot == False:
            embed = discord.Embed(title="Help Menu", color=ctx.author.color)
            embed.add_field(name="t!setdesc *text*", value="Setze eine beschreibung für deinen Server!", inline=False)
            embed.add_field(name="t!setchannel *channel*", value="Setze den Werbechannel! (keine Anforderungen)",
                            inline=False)
            embed.add_field(name="t!bump", value="Bumpe dein Server.", inline=False)
            embed.add_field(name="t!support", value="Supportserver einladung", inline=False)
            embed.add_field(name="t!invite", value="Bot einladung", inline=False)
            embed.set_footer(text='Do you need help? t!support', icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/522437022095245313/546359964101509151/Neko_Logo.png')
            embed.timestamp = datetime.utcnow()
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def support(self, ctx):
        if ctx.author.bot == False:
            channel = self.bot.get_channel(638414867656736770)
            invitelinknew = await channel.create_invite(xkcd=True, max_age=600, reason="Neko Dev. Support")
            embed = discord.Embed(color=ctx.author.color)
            embed.add_field(name="Support Server Invite Link", value="[Do you need help? Click me!]({})\n"
                                                                     "This link disapears in 10 minutes.".format(
                invitelinknew))
            embed.set_footer(text='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
            embed.timestamp = datetime.utcnow()
            await ctx.channel.send(embed=embed)

    @bot.command()
    async def invite(self, ctx):
        if ctx.author.bot == False:
            inv = "https://discordapp.com/api/oauth2/authorize?client_id=631149480464613406&permissions=117920&scope=bot"
            embed = discord.Embed(color=ctx.author.color)
            embed.add_field(name="{} Invite link".format(self.bot.user.name),
                            value="[Do you like invite me? Click here!]({})".format(inv))
            embed.set_footer(text='Do you need help? t!support', icon_url=ctx.author.avatar_url)
            embed.timestamp = datetime.utcnow()
            await ctx.channel.send(embed=embed)

    #########################################################################################################################
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        guilds = list(s for s in self.bot.guilds)
        member = sum(len(s.members) for s in self.bot.guilds)
        channel1 = self.bot.get_channel(680175333148065835)
        channel4 = self.bot.get_channel(680175369885581399)
        await channel1.edit(name="Totalusers : {}".format(member))
        await channel4.edit(name="Server: {}".format(str(len(guilds))))

    #########################################################################################################################
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guilds = list(s for s in self.bot.guilds)
        member = sum(len(s.members) for s in self.bot.guilds)
        channel1 = self.bot.get_channel(680175333148065835)
        channel4 = self.bot.get_channel(680175369885581399)
        await channel1.edit(name="Totalusers : {}".format(member))
        await channel4.edit(name="Server: {}".format(str(len(guilds))))

    #########################################################################################################################

    @commands.command()
    async def statsetup(self, ctx):
        guilds = list(s for s in self.bot.guilds)
        member = sum(len(s.members) for s in self.bot.guilds)
        channel1 = self.bot.get_channel(680175333148065835)
        channel4 = self.bot.get_channel(680175369885581399)
        await channel1.edit(name="Totalusers : {}".format(member))
        await channel4.edit(name="Server: {}".format(str(len(guilds))))


def setup(bot):
    bot.add_cog(cmd(bot))
