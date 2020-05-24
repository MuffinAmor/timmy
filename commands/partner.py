from time import time

import discord
from discord.ext import commands

from lib.general import check_dbl_vote
from lib.general import edit_time
from lib.general import get_time
from lib.settings import del_channel
from lib.settings import del_desc
from lib.settings import request_author
from lib.settings import request_channel
from lib.settings import request_desc
from lib.settings import request_invite
from lib.settings import set_channel
from lib.settings import set_desc
from lib.settings import set_invite

bot = commands.Bot(command_prefix='t!')

botcolor = 0x000ffc

bot.remove_command('help')


class partner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def setchannel(self, ctx, channel: discord.TextChannel):
        if channel == None:
            await ctx.send("Bitte wähle einen Channel aus!")
        else:
            await ctx.send(set_channel(str(ctx.guild.id), str(channel.id)))

    @bot.command()
    async def bump(self, ctx):
        if not ctx.author.bot:
            sid = str(ctx.guild.id)
            voted = check_dbl_vote(str(ctx.author.id))
            url = "https://top.gg/bot/631149480464613406/vote"
            total_user = len(list(member for member in ctx.guild.members if not member.bot))
            el = len(list(emojis.name for emojis in ctx.guild.emojis))
            rl = len(list(role.mention for role in ctx.guild.roles if not role.name == "@everyone"))
            owner = ctx.guild.owner.name
            if voted == True:
                zeit = 14400
                msg = ""
                msg2 = ""
            else:
                zeit = 43200
                msg = "Du kannst die Wartezeit für den nächsten Bump auf 4 Stunden verkürzen indem du uns mit einem" \
                      " [Vote]({}) unterstützt.".format(url)
                msg2 = "Du kannst auch sofort bumpen, indem du uns mit einem [Vote]({}) unterstützt.".format(url)
            if request_channel(sid) == None:
                await ctx.send("Du musst erst einen Channel setzen bevor du bumpen kannst!")
            elif request_desc(sid) == None:
                await ctx.send("Ops, du hast wohl vergessen deine Serverbeschreibung einzustellen!")
            elif round(time() - get_time(sid)) < zeit:
                sekunden = zeit - round(time() - get_time(sid))
                if sekunden < 60:
                    embed = discord.Embed(
                        description='Du musst noch: {} Sekunden warten bis du deinen Server bumpen kannst.\n'
                                    '{}'.format(
                            sekunden, msg2))
                    await ctx.send(embed=embed)
                elif sekunden < 3600:
                    minutes = sekunden // 60
                    seconds = sekunden - 60 * minutes
                    embed = discord.Embed(
                        description='Du musst noch: {} Minuten und {} Sekunden warten bis du deinen Server bumpen kannst.\n'
                                    '{}'.format(
                            minutes, seconds, msg2))
                    await ctx.send(embed=embed)
                elif sekunden < 21600:
                    hours = sekunden // 3600
                    minutes = (sekunden - 3600 * hours) // 60
                    seconds = sekunden - 3600 * hours - 60 * minutes
                    embed = discord.Embed(
                        description='Du musst noch: {} Stunden, {} Minuten und {} Sekunden warten bis du deinen Server bumpen kannst.\n'
                                    '{}'.format(
                            hours, minutes, seconds, msg2))
                    await ctx.send(embed=embed)
                else:
                    hours = sekunden // 3600
                    minutes = (sekunden - 3600 * hours) // 60
                    seconds = sekunden - 3600 * hours - 60 * minutes
                    embed = discord.Embed(
                        description='Du musst noch: {} Stunden, {} Minuten und {} Sekunden warten bis du deinen Server bumpen kannst.\n'
                                    '{}'.format(
                            hours, minutes, seconds, msg))
                    await ctx.send(embed=embed)
            else:
                desc = request_desc(sid)
                authorid = request_author(sid)
                user = self.bot.get_user(authorid)
                if user == None:
                    author = "Unbekannt"
                else:
                    author = user
                try:
                    inv = await ctx.guild.invites()
                    for i in inv:
                        if i:
                            set_invite(sid, i.url)
                            break
                except:
                    await ctx.send("Ich kann leider nicht auf deine Invites zugreifen!\n"
                                   "Bitte gebe mir die erforderlichen Rechte dazu!")
                    return
                edit_time(sid)
                invite = request_invite(sid)
                try:
                    embed = discord.Embed(title="Server Bump!", color=ctx.author.color)
                    embed.add_field(name="Server Infos", value="__Owner__: {}\n"
                                                               "__Nutzer__: {}\n"
                                                               "__Rollen__: {}\n"
                                                               "__Emotes__: {}\n".format(owner, total_user, rl, el), inline=False)
                    embed.add_field(name=ctx.guild.name, value="{}\n"
                                                               "Author: {}\n"
                                                               "Invite: {}".format(desc, author, invite,
                                                                                   inline=False))
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.set_footer(text="Bump", icon_url=ctx.guild.icon_url)
                    for server in self.bot.guilds:
                        try:
                            sid2 = str(server.id)
                            channelid = request_channel(sid2)
                            if not channelid == None:
                                channel = self.bot.get_channel(int(channelid))
                                if channel:
                                    try:
                                        await channel.send(embed=embed)
                                    except Exception as e:
                                        print(e)
                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)
                embed = discord.Embed(
                    description="{} wurde erfolg gebumpt!\n"
                               "{}".format(ctx.guild.name, msg))
                await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("t!setdesc"):
            if message.author.guild_permissions.administrator == True:
                msg = message.content.replace("t!setdesc", "")
                if len(message.content) <= 50:
                    await message.channel.send("Die Beschreibung ist zu kurz, bitte schreibe mindestens 50 Zeichen.")
                else:
                    await message.channel.send(set_desc(message.author.id, str(message.guild.id), msg))
            else:
                pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        sid = str(channel.guild.id)
        if not request_channel(sid) == None:
            chan = request_channel(sid)
            if chan == str(channel.id):
                del_channel(sid)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        sid = str(guild.id)
        if not request_desc(sid) == None:
            del_desc(sid)
            del_channel(sid)


def setup(bot):
    bot.add_cog(partner(bot))
