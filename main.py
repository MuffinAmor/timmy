import asyncio
import json
import os

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or('t!'))

os.chdir(r'/home/niko/data/')


def token():
    with open("Timmy/token.json", 'r') as fp:
        data = json.load(fp)
    Token = data['token']
    return str(Token)


TOKEN = str(token())

botcolor = 0xffffff

bot.remove_command('help')
########################################################################################################################

extensions = ['commands.auto', 'commands.cmd', 'commands.partner', 'commands.dbl']


@bot.event
async def on_ready():
    print('--------------------------------------')
    print('Bot is ready.')
    print('Eingeloggt als')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------------------------')
    bot.loop.create_task(status_task())


########################################################################################################################
async def status_task():
    while True:
        servers = list(bot.guilds)
        await bot.change_presence(activity=discord.Game('t!help | Timmy'))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Game('#NDC Project'))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Game('t!help | Timmy'))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Game('with {0} Server.'.format(len(servers))))
        await asyncio.sleep(15)
    ########################################################################################################################


@bot.command()
@commands.is_owner()
async def goodnight(ctx):
    await ctx.channel.send("Sleep well")
    await bot.logout()


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        bot.load_extension(extension)
        print('{} wurde geladen.'.format(extension))
        embed = discord.Embed(
            title='{} wurde geladen.'.format(extension),
            color=botcolor
        )
        msg = await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await msg.delete()
    except Exception as error:
        print('{} konnte nicht geladen werden. [{}]'.format(extension, error))
        embed = discord.Embed(
            title='{} konnte nicht geladen werden. [{}]'.format(extension, error),
            color=botcolor
        )
        msg = await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await msg.delete()


########################################################################################################################
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    try:
        bot.unload_extension(extension)
        print('{} wurde deaktiviert.'.format(extension))
        embed = discord.Embed(
            title='{} wurde deaktiviert.'.format(extension),
            color=botcolor
        )
        msg = await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await msg.delete()
    except Exception as error:
        print('{} konnte nich deaktiviert werden. [{}]'.format(extension, error))
        embed = discord.Embed(
            title='{} konnte nicht deaktiviert werden. [{}]'.format(extension, error),
            color=botcolor
        )
        msg = await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await msg.delete()


########################################################################################################################
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    try:
        bot.unload_extension(extension)
        bot.load_extension(extension)
        await ctx.channel.send('{} wurde neu geladen.'.format(extension))
    except Exception as error:
        await ctx.channel.send('{} konnte nicht geladen werden. [{}]'.format(extension, error))


########################################################################################################################
if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} konnte nicht geladen werden. [{}]'.format(extension, error))

bot.run(TOKEN)
