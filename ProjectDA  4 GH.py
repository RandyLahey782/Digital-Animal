import discord
#import mysql.connector
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
from datetime import datetime
import utils
import sys
import os
from pathlib import Path
from googletrans import LANGUAGES
from Core.DA_methods import *
from Core.DA_requests import *
from itertools import compress
import tracemalloc
import asyncio
from typing import Union
import cmath
import itertools
import platform
import logging
import motor.motor_asyncio
from cryptography.fernet import Fernet
import time

#import utils.json
#from utils.mongo import Document

#'/home/pi/hydro/docs'
#C:\Users\New User\Desktop\SONA\DA\files\docs

TEXT_FILES = Path(r'C:\Users\New User\Desktop\SONA\DA\files\docs')
LSYS = Path(r'C:\Users\New User\Desktop\SONA\DA\files\docs')
COGS = Path(r'C:\Users\New User\Desktop\SONA\DA\files\cogs')
intents = discord.Intents.all()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix='$', intents=intents)
HF = 273255595509809162
stats2 = itertools.cycle(["I am Digital Animal!", "Version 2.5", "on {x} Servers",  "with {y} users", "Support: xAZEFBrsjq", "D-D-D-D-D-D-Digital Animal Freaky Folks"])

cogs = ["cogs.RPS", "cogs.Moderation", "cogs.Ping", "cogs.Level"]#, "cogs.Error"]

async def cogger():
    if __name__ == '__main__':
        for extension in cogs:
            await client.load_extension(extension, package=None)
            #print(extension)
            b = extension
           # print(f"{b[5:]} extension loaded")
            #print(f"The {b[5:]} extension was loaded")
            print("Extensions loaded")


#SHUTDOWN

@client.command()
async def shutdown(ctx):
    AZU = [273255595509809162, 773695202136686612, 1096531392369807492]
    for uz in AZU:
        if ctx.author.id in AZU:
    #try:
            await ctx.send("Adios")
            await client.close()
            time.sleep(5)
    #except discord.ext.commands.errors.NotOwner:
        #await ctx.send("lol")
        #return
        else:
            await ctx.send("lol")
            return
    return

#EVENTS

@client.event
async def on_ready():
    stat.start()
    tracemalloc.start()
    await cogger()
    #print("Loop Started")
    #client.mongo motor.motor_asyncio.AsyncIOMotorClient(str(client.connection_url))
    #client.db = client.mongo['DA1']
    #client.config = Document(client.db, 'config')
    #print("db up")
    #for document in await client.config.get_all():
    # print (document)
    print("Digital Animal, online")


@tasks.loop(minutes=1)
async def stat():
    n = next(stats2)
    n2 = n.format(x=len(client.guilds), y=sum([len(guild.members) for guild in client.guilds]))
    await client.change_presence(activity=discord.Game(name=n2))
    return


@client.event
async def on_message(message):
    mid = message.guild.id
    if message.author.bot:
        return
    else:
        if message.content.lower() == '$help':
            await message.channel.send("Please use `$cmds`")
            return

        else:
            #try:
            #print("1")
            msg = message.content.lower()
            #cag = message_events(mid, message.content.lower())
            #if cag:
            x = GetMB(mid, msg)
            if x is not None:
                await message.channel.send(f'{x}')

            else:
                pass


                #await message.channel.send(f'{cag}')

            #except Exception as e:
            #    print("Exception")
            #    return


    await client.process_commands(message)


@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    try:
        channel = GestapoChannel(before.guild.id)
    except NeedInstallFirst:
        #print('Message edit need to install! <install_spy>')
        return

    if channel is not None:
        ch = client.get_channel(channel)

        if len(before.embeds) != 0:
            pass


        else:
            embed = discord.Embed(
                title='Message has been edited',
                description=f'`{str(before.author)}` edited a message on Server: ',
                colour=0xdd16d9
                )
            embed.add_field(name='Server :',value=f'`{str(before.guild)}`', inline=False)
            embed.add_field(name='Channel :',value=f'`{str(before.channel)}`', inline=False)
            embed.add_field(name='Message Before :',value=f'`{before.content}`')
            embed.add_field(name='Message After :',value=f'`{after.content}`')
            embed.set_footer( text=f'Time of Edit : {datetime.now().strftime("%H:%M:%S")}')
            await ch.send(embed=embed)


@client.event
async def on_message_delete(message):
    try:
        channel = GestapoChannel(message.guild.id)
        #print("ch:", channel)
    except NeedInstallFirst:
        #print('Message delete need to install! <install_spy>')
        return

    if message.author == client.user:
        return

    if channel is not None:
        ch = client.get_channel(channel)
        #print(ch)

        if len(message.embeds) != 0:
            return

        if message.attachments:
            embed=discord.Embed(
                title='Message has been deleted',
                description=f'`{message.author}` deleted a message',
                colour=0xdd16d9
            )
            embed.add_field(name='Attachment :',value=f'{message.attachments[0].url}', inline=False)
            embed.add_field(name='Server:',value=f'`{message.guild}`', inline=False)
            embed.add_field(name='Channel:',value=f'`{message.channel}`', inline=False)
            embed.set_footer(text=f'Time: {datetime.now().strftime("%H:%M:%S")}')
            await ch.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Message has been deleted',
                description=f'`{message.author}` deleted a message',
                colour=0xdd16d9
                )
            embed.add_field(name='Server :',value=f'`{message.guild}`', inline=False)
            embed.add_field(name='Channel :',value=f'`{message.channel}`', inline=False)
            embed.add_field(name='Message :',value=f'`{message.content}`', inline=False)
            embed.set_footer(text=f'Time: {datetime.now().strftime("%H:%M:%S")}')
            await ch.send(embed=embed)


@client.event
async def on_member_update(before, after):

    def check_roles() -> Union[Tuple[str, dict], None]:

        before_roles = [role.name for role in before.roles]
        after_roles = [role.name for role in after.roles]

        removed_roles = set(before_roles) - set(after_roles)
        upgrade_roles = set(after_roles) - set(before_roles)

        if upgrade_roles:
            return 'Upgrade', ''.join(list(upgrade_roles))
        elif removed_roles:
            return 'Removed', ''.join(list(removed_roles))
        else:
            return None

    def check_nick() -> bool:
        if before.nick != after.nick:
            return True
        else:
            return False

    def check_avatar():
        if before.avatar != after.avatar:
            return True
        else:
            return False
    try:
        channel = update_get_channel(before.guild.id)
    except NeedInstallFirst:
        #print('update member command has to install <install_updates>')
        return

    #try:
        #unc = StatsBlyatX(before.user.id, before.guild.id, s)
    #except Exception:
        #print(Exception)
        #return

    if before.nick == client.user:
        return

    if channel is not None:
        ch = client.get_channel(channel)
        if check_roles() or check_nick() or check_avatar():
            embed = discord.Embed(
                title='User Updates', description=f'`{before.display_name}` Profile Update', colour=0xdd16d9)

        if check_roles() is not None:
            embed.add_field(name=f'`{check_roles()[0]}` role', value=f'`{check_roles()[1]}`', inline=False)
            embed.set_footer(text=f'Time : {datetime.now().strftime("%H:%M:%S")}')
            await ch.send(embed=embed)
        if check_nick():
            #if unc is not None:
                #print("change name")

            embed.add_field(name='Before:', value=f'From `{before.nick}` ')
            embed.add_field(name='After:', value=f'To `{after.nick}`')
            embed.set_footer(text=f'Time : {datetime.now().strftime("%H:%M:%S")}')
            await ch.send(embed=embed)
            return

        if check_avatar():
            #embed.add_field(name='Avatar Before', value=f'from {before.avatar}')
            #embed.add_field(name='After Avatar', value=f'To {after.avatar}')
            #embed.set_footer(text=f'Time : {datetime.now().strftime("%H:%M:%S")}')
            #await ch.send(embed=embed)
            return


@client.event
async def on_guild_join(guild):
    SI = guild.id
    SN = guild.name
    SMz = sum([len(guild.members)])
    ch = 706276748924420136
    channel = client.get_channel(ch)
    #UpdateGuild(SI, SN, SMz)
    print("Digital Animal has joined {}".format(SN))
    await channel.send(f"Digital Animal has joined `{SN}`\nServerID: `{SI}`\nMember Count: `{SMz}`")
    return


@client.event
async def on_member_join(member):
    try:
        channel = port_get_channel(member.guild.id)
    except NeedInstallFirst:
        #print('on member must install by <install_welcome>')
        return

    try:
        check_ar = CheckAR(member.guild.id)
        #print(check_ar)
    except Exception:
        return


    if channel is not None:
        if check_ar is not None:
            ar = discord.utils.get(member.guild.roles, id=check_ar)
            await member.add_roles(ar)

            ch = client.get_channel(channel)
            embed = discord.Embed(title='**Member Joined!**',description=f'{member}', colour=0x2ecc71)
            embed.add_field(name='Account Creation Date:',value=f'{member.created_at.strftime("%A, %B %#d, %Y, %H:%M UTC")}', inline=False)
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f'Time of join: {datetime.now().strftime("%H:%M:%S")}')
            await ch.send(embed=embed)
            return

        else:
            ch = client.get_channel(channel)
            embed = discord.Embed(title='**Member Joined!**',description=f'{member}', colour=0x2ecc71)
            embed.add_field(name='Account Creation Date:',value=f'{member.created_at.strftime("%A, %B %#d, %Y, %H:%M UTC")}', inline=False)
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f'Time of join: {datetime.now().strftime("%H:%M:%S")}')
            await ch.send(embed=embed)
            return
    else:
        #print("no channel")
        return


@client.event
async def on_member_remove(member):
    try:
        channel = port_get_channel(member.guild.id)
        #print(channel)
    except NeedInstallFirst:
        #print('remove member commad has to install <install_goodbye>')
        return

    if channel is not None:
        #x = get_pme[0]
        #y = EraseBlyat2(PME)
        ch = client.get_channel(channel)
        embed = discord.Embed(title='**Member left!**', colour=0xe67e22)
        embed.add_field(name=f'{member} left ***{member.guild}***', value='Bye!', inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f'Time of Leave: {datetime.now().strftime("%H:%M:%S")}')
        await ch.send(embed=embed)
        return

    else:
        #print("no channel")
        return
        #if channel is not None:
            #ch = client.get_channel(channel)
            #embed = discord.Embed(title='**Member Left!**', colour=0x090909)
            #embed.add_field(name=f'{member} left ***{member.guild}***', value='Bye', inline=False)
            #embed.set_thumbnail(url=member.avatar_url)
            #embed.set_footer(text=f'Time of Leave: {datetime.now().strftime("%H:%M:%S")}')
            #await ch.send(embed=embed)
            #return


#HELP COMMAND
@client.command()
async def cmds(ctx, sector=None):
    if not sector:
        await ctx.send("$cmds mod\n$cmds level\n$cmds public\n$cmds admin\n$cmds help")
        return

    if sector == 'mod':
        embed = discord.Embed(
            title='***DIGITAL ANIMAL***\n**Moderation Commands**',
            description='Some commands require user-passed arguments\nThese commands require bot/user admin/other perms\nCertain commands require DA role above all normal roles',
            colour=discord.Color.random()
        )
        embed.add_field(name='addrole [@member] [@role]', value='Gives a role to specified user', inline=False)
        embed.add_field(name ='delrole [@member] [@role]', value='Removes a role from a specified user', inline=False)
        embed.add_field(name='ban [@member]', value='Bans a user', inline=False)
        embed.add_field(name='addmsg [term] [def]', value='Create server-local terms', inline=False)
        embed.add_field(name='delmsg [term]', value='Remove term', inline=False)
        embed.add_field(name='kick [@member]', value='Kicks a user', inline=False)
        embed.add_field(name='clear [2+]', value='Clears messages', inline=False)
        embed.add_field(name='mute [@member] [#s, #m, #h, #d]', value='Mutes a user for a specified time\nMust fully disable @everyone role', inline=False)
        embed.add_field(name='unmute [@member]', value='Unmutes a user', inline=False)
        embed.add_field(name='nuke', value='Nukes a channel, may take some time', inline=False)
        embed.add_field(name='timeout [@member]', value='Puts a user in JAIL', inline=False)
        embed.add_field(name='free [@member]', value='Frees user from JAIL', inline=False)
        embed.add_field(name='warn [@member] [warning]', value='Warns a user', inline=False)
        await ctx.send(embed=embed)
        return

    elif sector == 'level':
        embed = discord.Embed(
            title='***DIGITAL ANIMAL***\n**Level Commands**',
            description='Anything related to level requires `$inst_lsys`',
            colour=discord.Color.random()
        )
        embed.add_field(name='lb', value='Opens leaderboard', inline=False)
        embed.add_field(name='stats', value='Opens level statistics', inline=False)
        embed.add_field(name='apz', value='Open list of registered users', inline=False)
        embed.add_field(name='bankacc', value='Opens server account', inline=False)
        embed.add_field(name='rob [@mention]', value='Steal exp command', inline=False)
        embed.add_field(name='reset [@mention]', value='Resets a users stats, completely', inline=False)
        embed.add_field(name='remove [member id]', value='Removes user from database', inline=False)
        embed.add_field(name='gpz [@member] [int]', value='Award points', inline=False)
        embed.set_footer(text='Rank 1 = 10 exp, Rank 2 = 1000 exp, \nRank 3 = 2500 exp, Rank 4 = 4000 exp, \nRank 5 = 5500 exp, Rank 6 = 7000 exp')
        #rank 2 = 500, rank 3 = 1000, rank 4 = 1750, rank 5 2500, rank 6 = 3500, rank 7 = 4500, rank 8 = 5750, rank 9 = 7000, rank 10 = 8500, rank 11 = 10000
        await ctx.send(embed=embed)
        return

    elif sector == 'admin':
        embed = discord.Embed(
            title='***DIGITAL ANIMAL***\n**Administrator Commands**',
            description='All commands require bot/user admin`',
            colour=discord.Color.random()
        )
        embed.add_field(name='ar_on [role name]', value='Autorole-on [role name(str)]', inline=False)
        embed.add_field(name='ar_off', value='Autorole off', inline=False)
        embed.add_field(name='inst_lsys', value='Installs level sytem', inline=False)
        embed.add_field(name='del_lsys', value='Uninstalls level system', inline=False)
        embed.add_field(name='inst_port', value='Installs welcome/goodbye channel', inline=False)
        embed.add_field(name='del_port', value='Uninstalls port channel', inline=False)
        embed.add_field(name='inst_spy', value='Installs Gestapo', inline=False)
        embed.add_field(name='del_spy', value='Uninstalls Gestapo', inline=False)
        embed.add_field(name='inst_updz', value='Installs member updates', inline=False)
        embed.add_field(name='del_updz', value='Uninstalls member updates channel', inline=False)
        embed.add_field(name='inst_modch', value='Installs moderation log channel', inline=False)
        embed.add_field(name='del_modch', value='Uninstalls mod channel', inline=False)
        await ctx.send(embed=embed)
        return

    elif sector == 'public':
        embed = discord.Embed(
            title='***DIGITAL ANIMAL***\n**Public Commands**',
            description='More cmds in-development`',
            colour=discord.Color.random()
        )
        embed.add_field(name='serverinfo', value='Display server info', inline=False)
        embed.add_field(name='userinfo', value='Display member info', inline=False)
        embed.add_field(name='av [@mention]', value='Display users avatar', inline=False)
        embed.add_field(name='ping', value='Ping latency', inline=False)
        embed.add_field(name='rolescount', value='Displays server roles', inline=False)
        embed.add_field(name='membercount', value='Displays number of members', inline=False)
        embed.add_field(name='define [word]', value='Urban Dictionary command', inline=False)
        embed.add_field(name='math [method [var] [var]', value='Math command', inline=False)
        embed.add_field(name='terms', value='Shows list of server terms', inline=False)
        await ctx.send(embed=embed)
        return

    elif sector == 'help':
        await ctx.send("`Support Server Invite: https://discord.gg/xAZEFBrsjq`")
        return

    else:
        return

#MOD COMMANDS

@client.command(aliases=['ar'])
@commands.has_permissions(administrator=True)
async def ar_on(ctx, *,rname=None):
    if not rname:
        await ctx.send("`You must pass in a role name (str)`")
        return
    else:
        perm1 = discord.Permissions(send_messages=True, read_messages=True, embed_links=True, add_reactions=True, attach_files=True, read_message_history=True)
        guild = ctx.guild
        gid = ctx.guild.id
        try:
            nr = await guild.create_role(name=rname, permissions=perm1)
            #print(nr.id)
            Upd_jr(gid, nr.id)
            #print("updated")
            await ctx.send(f"Role created, <@&{nr.id}> Whenever a new user joins, they will recieve this role")
            return
        except Exception as e:
            await ctx.send(e)
            return
#discord.ext.commands.errors.MissingRequiredArgument
@ar_on.error
async def ar_on_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("`You must @mention a user`")
        return
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("`Missing permissions, you must be admin`")
        return


@client.command(aliases=['unar'])
@commands.has_permissions(administrator=True)
async def ar_off(ctx):
    #try:
    if Del_jr(ctx.guild.id):
        await ctx.send("Autorole turned off, new user joins will not be given a role")
    #except Exception:
        #await ctx.send(Exception)

@ar_off.error
async def ar_off_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("`Missing permissions, you must be admin`")
        return


@client.command()
@commands.has_permissions(manage_messages=True)
async def addmsg(ctx, term: str, *,mg: str):
    guild = ctx.guild
    gid = ctx.guild.id
    ga = ctx.guild.name
    UpdateMB(ga, gid, term, mg)
    await ctx.send(f"Term added, `{term}`")
    return

@addmsg.error
async def addmsg_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("`You must pass in all required arguments`")
        return
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("`Missing permissions, you must have manage_messages permission`")
        return

@client.command()
@commands.has_permissions(manage_messages=True)
async def delmsg(ctx, term: str):
    guild = ctx.guild
    gid = ctx.guild.id
    EraseMB(gid, term)
    await ctx.send(f'Term removed, `{term}`')
    return


@client.command()
#@commands.has_permissions(manage_messages=True)
async def terms(ctx):
    LT = TimeNahui()
    cont = ReadMB()
    SID = ctx.guild.id
    tz = GetTerms(SID)
    #print(f'{tz}')
    try:
        ps = []
        for number, items in enumerate(tz, 1):
            pc = ""
            for item in items:
                pc += f'{item}'
            ps.append(f' {number}  `{pc}`')

        embed = discord.Embed(
        title=f'***DIGITAL ANIMAL***\nRegistered terms of {ctx.guild.name}',
        colour=discord.Color.random()
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text=f'Time: {LT}')
        embed.add_field(name=f'`№ | Term`', value='\n'.join(str(v) for v in ps), inline=False)
        await ctx.send(embed=embed)
        return
    except Exception as e:
        await ctx.send(e)
        return


@client.command(aliases=['moderate'])
@commands.has_permissions(administrator=True)
async def inst_modch(ctx):
    Asapk = ctx.guild.id #server ID
    Asapk0 = ctx.guild
    Ja = ctx.channel.id #channel ID
    Ja2 = ctx.channel.name
    #print(Asapk, Ja)
    ch = UpdateMod(Asapk, Ja) #upload server ID and channel ID
    await ctx.send("Moderation channel set, `{}`".format(Ja2))
    return

@inst_modch.error
async def inst_modch_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("`Missing permissions, you must be admin`")
        return


@client.command()
@commands.has_permissions(administrator=True)
async def del_modch(ctx):
    Asapk = ctx.guild.id #server ID
    Asapk0 = ctx.guild
    Ja = ctx.channel.id #channel ID
    Ja2 = ctx.channel.name
    aso = EraseMod(Ja)
    if aso:
        await ctx.send('`Moderation channel unset`')
        return

@del_modch.error
async def del_modch_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("`Missing permissions, you must be admin`")
        return


@client.command()
@commands.has_permissions(administrator=True)
async def inst_lsys(ctx):
    try:
        bal = 1000
        UpdateLCh(ctx.guild.id, ctx.channel.id, bal)
        await ctx.send('`Level updates installed successfully!`')
        #@break
        return

    except:
        await ctx.send("Blyat, I need permission!")
        return

@inst_lsys.error
async def inst_lsys_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("`Missing permissions, you must be admin`")
        return


@client.command()
@commands.has_permissions(administrator=True)
async def del_lsys(ctx):
    aso = EraseLCh(ctx.guild.id)
    if aso:
        await ctx.send('`Level updates uninstalled successfully`')
        return

@del_lsys.error
async def del_lsys_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("`Missing permissions, you must be admin`")
        return


@client.command()
@commands.has_permissions(administrator=True)
async def inst_spy(ctx):
    UpdateGestapo(ctx.guild.id, ctx.channel.id)
    await ctx.send('`Spy events installed successfully!`')

@inst_spy.error
async def inst_spy_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("`Missing permissions, you must be admin`")
        return


@client.command()
@commands.has_permissions(administrator=True)
async def del_spy(ctx):
    aso = NoGestapo(ctx.guild.id)
    if aso:
        await ctx.send('`Spy events uninstalled successfully`')
        return

@del_spy.error
async def del_spy_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("`Missing permissions, you must be admin`")
        return


@client.command()
@commands.has_permissions(administrator=True)
async def inst_port(ctx):
    update_port(ctx.guild.id, ctx.channel.id)
    await ctx.send('`Welcome event installed successfully!`')

@inst_port.error
async def inst_port_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("`Missing permissions, you must be admin`")
        return


@client.command()
@commands.has_permissions(administrator=True)
async def del_port(ctx):
    del_port(ctx.guild.id)
    await ctx.send('`Welcome event uninstalled successfully`')
    return

@del_port.error
async def del_port_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("`Missing permissions, you must be admin`")
        return


@client.command()
@commands.has_permissions(administrator=True)
async def inst_updz(ctx):
    update_update(ctx.guild.id, ctx.channel.id)
    await ctx.send('`Member update event installed successfully!`')

@inst_updz.error
async def inst_updz_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("`Missing permissions, you must be admin`")
        return


@client.command()
@commands.has_permissions(administrator=True)
async def del_updz(ctx):
    un_update(ctx.guild.id)
    await ctx.send('`Member updates uninstalled successfully`')
    return

@del_updz.error
async def del_updz_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("`Missing permissions, you must be admin`")
        return

#PUBLIC COMMANDS

@client.command(aliases=["server"])
async def serverinfo(ctx):
    Memberz = MembersBlyat(ctx)
    def get_channels():
        TotalTextBlyat = len(ctx.guild.text_channels)
        return TotalTextBlyat
    def get_channels2():
        TotalVoiceBlyat = len(ctx.guild.voice_channels)
        return TotalVoiceBlyat
    def ChannelsByat():
        Blyat1 = get_channels()
        Blyat2 = get_channels2()
        TotalNahui = (Blyat1 + Blyat2)
        return TotalNahui
    embed = discord.Embed(
        colour=discord.Color.random()
    )
    embed.set_author(name=f'DIGITAL ANIMAL\nServer Information')
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar.url)
    embed.set_thumbnail(url=ctx.guild.icon.url)

    embed.add_field(name='Server Name:', value=f'`{ctx.guild}`', inline=False)
    embed.add_field(name='Server ID:', value=f'`{ctx.guild.id}`', inline=False)
    embed.add_field(name='Server Owner:',value=f'`{ctx.guild.owner}`', inline=False)
    embed.add_field(name='Server Creation Date:',value=f'`{ctx.guild.created_at.strftime("%A, %B %#d, %Y, %H:%M UTC")}`', inline=False)
    embed.add_field(name=f'Number of members:',value=f'`{Memberz}`', inline=False)
    embed.add_field(name=f'Number of channels:',value=f'`{ChannelsByat()}`', inline=False)
    embed.add_field(name=f'Number of roles',value=f'`{ServerRolesBlyat(ctx)}`', inline=False)
    await ctx.send(embed=embed)




@client.command(aliases=['user'])
async def userinfo(ctx, user: discord.Member=None):
    pl1 = ["administrator", "manage_messages", "manage_guild", "mute_members", "kick_members", "ban_members", "mention_everyone", "manage_nickname", "manage_nicknames", "manage_roles", "view_audit_log"]
    pl2 = ["create_instant_invite", "read_messages", "send_messages", "add_reactions", "embed_links", "external_emojis", "attach_files", "change_nickname", "connect", "speak"]
    if user is None:
         member = ctx.message.author
         perm_list = [perm[0] for perm in member.guild_permissions if perm[1]]

         return
    else:
        member = user
        perm_list = [perm[0] for perm in member.guild_permissions if perm[1]]
        result = list(set(perm_list) & set(pl1))
        result2 = list(set(perm_list) & set(pl2))
        print(result2)
        x = ', '.join(result)
        y = ', '.join(result2)

        embed=discord.Embed(
            color=discord.Color.random()
        )
        embed.set_author(name=f'DA\nUser Information')
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name='Discord Username:',value=f'`{member.display_name}`', inline=False)
        embed.add_field(name='Discord User Discriminator:',value=f'`{member.discriminator}`', inline=False)
        embed.add_field(name='Discord User ID:',value=f'`{member.id}`', inline=False)
        embed.add_field(name='Account Creation Date:',value=f'`{member.created_at.strftime("%A, %B %#d, %Y, %H:%M UTC")}`', inline=False)
        embed.add_field(name="Major Permissions:", value=f'`{x}`', inline=False)
        embed.add_field(name='Minor Permissions:', value=f'`{y}`', inline=False)
        embed.set_footer(text="If you do not see a perm for minor perms, assume you have it")
        await ctx.send(embed=embed)
            #await ctx.send('\n'.join(str(v) for v in perm_list))
        





@client.command(aliases=["def"])
async def define(ctx, *, term=None):
    #await ctx.send("Sorry this is unavailable atm")
    if term is None:
        await ctx.send("You need to pass in a word")
        return
    else:
        try:
            x, y = get_urban(term)
            embed = discord.Embed(
                    title='***DIGITAL ANIMAL***\n*Define*',
                    description=f'**Word**: `{term}`',
                    colour=0x1225d6
                )
            embed.add_field(name='Defined with URBAN DICTIONARY',
                                value=x, inline=False)
            embed.add_field(name='Example:', value=y, inline=False)
            embed.add_field(name='For more information, click this safe link!', value=f'https://www.urbandictionary.com/define.php?term={term}', inline=False)
            await ctx.send(embed=embed)
            return
        except (discord.errors.HTTPException, TypeError) as e:
            embed=discord.Embed(
            title='Exception in command DEFINE',
            description = f'`{e}`',
            colour=0x090909
            )
            await ctx.send(embed=embed)
            return
        except Exception as e:
            embed=discord.Embed(
            title='Exception in command DEFINE',
            description = f'`{e}`',
            colour=0x090909
            )
            await ctx.send(embed=embed)
            return


        #else: 




@client.command(aliases=["avatar"])
@commands.cooldown(1, 6, commands.BucketType.user)
async def av(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("@mention")
        return
    else:
        show_avatar = discord.Embed(

            color=0x1ad16a
        )
        show_avatar.set_image(url='{}'.format(member.avatar.url))
        await ctx.send(embed=show_avatar)
        return



@client.command(pass_context=True)
@commands.cooldown(1, 6, commands.BucketType.user)
async def kill(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("kill who?")
    else:
        if member == 879212965050585099:
            await ctx.send("I will not kms!")

        else:
            await ctx.send(f"*{member.name} has been killed*")
 

@client.command(pass_context=True)
@commands.cooldown(1, 3, commands.BucketType.channel)
async def say(ctx, *,msg=None):
    try:
        await ctx.channel.purge(limit=1)
    except:
        pass


    if not msg:
        await ctx.send("Say what?")
        return
    else:
        embed= discord.Embed(
        color=discord.Color.random(),
        title=f'{msg}'
        )
        await ctx.send(embed=embed)
        return


@client.command()
async def membercount(ctx):
    bots = len([bot for bot in ctx.guild.members if bot.bot])
    members = len([member for member in ctx.guild.members if not member.bot])
    await ctx.send(f'There are {bots} bots and {members} members in {ctx.guild}\nTotal members: {bots + members}')



@client.command()
async def rolescount(ctx):
    gr = [str(role.name) for role in ctx.guild.roles]
    grn = ServerRolesBlyat(ctx)
    #grn = len(gr)
    embed = discord.Embed(
    title=f'Roles for {ctx.guild.name}',
    description=f'There are {grn}',
    colour=discord.Color.random()
    )
    embed.add_field(name='Roles: ', value=f'`{gr}`', inline=False)
    try:
        return await ctx.send(embed=embed)
    except Exception:
        return await ctx.send(f"there are {grn} roles in this server")



@client.command()
async def servers(ctx):
    def CServersBlyat():
         D1 = len(client.guilds)
         D3 = list(client.guilds)
         d3 = '\n'.join(str(guild.name) for guild in D3)
         d4 = '\n'.join(str(guild.id) for guild in D3)
         #print(d4)
         #print(d3)
         return D1, d3
    D2, D4 = CServersBlyat()
    #await ctx.send(f'Digital Animal is in {D2} servers')
    embed = discord.Embed(
    title='***DIGITAL ANIMAL***\nServers',
    description=D2,
    color=discord.Color.random()
    )
    embed.add_field(name='Server List:', value=f'`{D4}`', inline=False)
    await ctx.send(embed=embed)

    return



@client.command()
async def invz(ctx):
    invites = []

    for guild in client.guilds:
        for c in guild.text_channels:
            if c.permissions_for(guild.me).create_instant_invite:  # make sure the bot can actually create an invite
                invite = await c.create_invite()
                invites.append(invite)
            print(invites)
            break

                #break  # stop iterating over guild.text_channels, since you only need one invite per guild



@client.command(pass_context=True)
async def math(ctx, method: str, n1: float, n2: float):
    methods = {
        'add': lambda n1, n2: '{:.2f}'.format(n1+n2),
        'sub': lambda n1, n2: '{:.2f}'.format(n1-n2),
        'multi': lambda n1, n2: '{:.2f}'.format(n1*n2),
        'div': lambda n1, n2: '{:.3f}'.format(n1/n2),
        'power': lambda n1, n2: n1**n2
    }
    if method.lower() == 'power':
        if len(str(n1)) > 3 or len(str(n2)) > 3:
            await ctx.send("Number too big, sorry I cannot compute that")
            return
    if method.lower() == 'div' and n2 == 0:
        await ctx.send("Cannot divide by 0")
        return

    else:

        await ctx.send(f'`{n1}` {method} `{n2}` is {methods[method](n1,n2)}')

@math.error
async def m_error(ctx, error):
    embed = discord.Embed(title='Usage for math command',description='methods = [add,sub,multi,div,power] [number] [number]',colour=0xdd16d9)
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)} Milliseconds')







