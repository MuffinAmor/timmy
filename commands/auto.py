from datetime import datetime

import discord
from discord.ext import commands

botcolor = 0x00ffff


class auto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counter = 0

    ########################################################################################################################
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            server = self.bot.get_guild(382290709249785857)
            try:
                inv = await server.invites()
            except:
                pass
            for invites in inv:
                if invites:
                    invite2 = invites.url
                    break
            else:
                invite2 = "https://discord.gg"
            self.counter = + 1
            channel = self.bot.get_channel(692781515045601402)
            await channel.send("*{}* keeps a error ```{}```".format(ctx.message.content, error))
            embed = discord.Embed(title="Ops, there is an error!",
                                  description="Error report Nr. {} after reset.".format(self.counter),
                                  color=botcolor)
            embed.add_field(name='Server:', value='{}'.format(ctx.message.guild), inline=True)
            embed.add_field(name='Command:', value='{}'.format(ctx.message.content), inline=False)
            embed.add_field(name='Error:', value="```python\n{}```".format(error), inline=False)
            embed.add_field(name='Problems?',
                            value='Take a Picture of this message and contact us [here]({}).'.format(invite2),
                            inline=True)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text='Error Message', icon_url=ctx.message.author.avatar_url)
            embed.timestamp = datetime.utcnow()
            await ctx.channel.send(embed=embed)
            print(error)

    #########################################################################################################################
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(692781491222085738)
        server_info1 = (datetime.now() - guild.created_at).days
        Bot = list(member.bot for member in guild.members if member.bot is True)
        user = list(member.bot for member in guild.members if member.bot is False)
        embed = discord.Embed(
            color=botcolor)
        embed.add_field(name='<:Neko_Logo:631245752722784283>__Server Join__<:Neko_Logo:631245752722784283>',
                        value='** **', inline=False)
        embed.add_field(name='Name:', value='{}'.format(guild.name), inline=True)
        embed.add_field(name='Server ID:', value='{}'.format(guild.id), inline=True)
        embed.add_field(name='Region:', value='{}'.format(guild.region), inline=True)
        embed.add_field(name='Membercount:', value='{} members'.format(guild.member_count), inline=True)
        embed.add_field(name='Botcount:', value='{} Bots'.format(str(len(Bot))), inline=True)
        embed.add_field(name='Humancount:', value='{} users'.format(str(len(user))), inline=True)
        embed.add_field(name='Large Server:', value='{} (250+ member)'.format(guild.large), inline=True)
        embed.add_field(name='Serverowner:', value='{}'.format(guild.owner), inline=True)
        embed.add_field(name='Verifylevel:', value='{} '.format(guild.verification_level), inline=True)
        embed.add_field(name='Created at:', value='{}'.format(
            "{} ({} days ago!)".format(guild.created_at.strftime("%d. %b. %Y %H:%M"), server_info1)), inline=False)
        embed.set_thumbnail(url="{0}".format(guild.icon_url))
        embed.set_footer(text='New Serverjoin', icon_url=guild.icon_url)
        embed.timestamp = datetime.utcnow()
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(692781491222085738)
        embed = discord.Embed(title="", description="Timmy leaved *{0}*".format(guild.name),
                              color=discord.Color.blurple(),
                              timestamp=datetime.utcnow())
        embed.set_footer(text='This message was requested by Neko')
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(auto(bot))
