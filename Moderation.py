import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
from Core.DA_methods import *
from dateutil.relativedelta import relativedelta
from asyncio import run_coroutine_threadsafe
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union
from copy import deepcopy
from discord.utils import get
import utils
import asyncio
import requests
import json
import re
import sys
import traceback
intents = discord.Intents.all()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix='$', intents=intents)
HF = 273255595509809162
DA = 879212965050585099
TEXT_FILES = Path(r'C:\Users\New User\Desktop\SONA\DA\files\docs')
time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}
#r'C:\Users\New User\Desktop\SONA\DA\files\docs'
#r'/home/pi/hydro/docs'

class NeedInstallFirst(Exception):
    pass


class ConvertBlyat(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*int(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! `h/m/s/d` are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time


class Admin_Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.InternalMute.start()

    def cog_unload(self):
        self.InternalMute.cancel()


    @tasks.loop(seconds=60)
    async def InternalMute(self):
        #print("Mute task started")
        LT = TimeNahui2()
        #print("Loop time:", LT)
        LTime = str(LT)
        content = self.ReadBlyat()
        content2 = deepcopy(content)
        for key, value in list(content2.items()):
            try:
                X = (value['timeMute'])
                Y = (value['muteTime'])
                Z = (value['serverID'])
                #print("ToM:", X)
                #print("PUT:", X + Y)

                FTime = (X + Y) #FTime = (time of mute + duration of mute)
            except Exception:
                print(Exception)
                return

            #if Y is None:
                #print("indef time, doing nothing")
                #return

            if LT >= FTime:  #if the current time upon task loop (CT) is greater than or equal to FTime
                guild = self.client.get_guild(value['serverID'])
                member = guild.get_member(value['memberID'])
                channels = (channel.id for channel in member.guild.channels)


                if len(member.roles) is not None: #if member has role(s)
                    Rx = (role for role in member.roles if role.name != '@everyone')
                    for role in Rx:
                        await member.remove_roles(role)
                        #print(member, "removed mute role")

                    restore = (discord.utils.get(member.guild.roles, id=role) for role in value['userRoles'])
                    for role in restore:
                        try:
                            print(role)
                            await member.add_roles(role)
                            self.EraseBlyat(member.id, Z)
                            print(member, "unmuted/removed from file, flawless")
                        except Exception:
                            print(Exception)
                            continue

                try:
                    MC = self.ChannelMod(member.guild.id)
                    #print(MC)
                except NeedInstallFirst:
                    print("Mod channel not set up")
                    return None

                if MC is not None:
                    ch = (discord.utils.get(member.guild.channels, id=MC) for channel in channels)
                    for channel in ch:
                        #print(channel)

                        embed = discord.Embed(
                            title='***DIGITAL ANIMAL***\n*Moderation*',
                            description='*Mute Period Over*',
                            color=discord.Colour.random()
                            )
                        embed.set_thumbnail(url=member.avatar.url)
                        embed.set_footer(text=f'Time of unmute: {TimeNahui()}')
                        embed.add_field(name=f'`Mute for {member} is over`', value=f'`Previous roles have been restored`', inline=False)
                        await channel.send(embed=embed)
                        return

                else:
                    pass

            else:
                continue


    @InternalMute.before_loop
    async def before_InternalMute(self):
        await self.client.wait_until_ready()


    @commands.Cog.listener()
    async def on_ready(self):
        print("Mute task started")
        self.InternalMute.start()


    def ChannelMod(self, Asapk: int) -> Union[int,None]: #gets channel
        content = ReadMod()

        get_mc = [content[i]['Channel']
                        for i in content if content[i]['Server'] == Asapk]

        if get_mc:
            return get_mc[0]
        else:
            return None


    def WriteBlyat(self, cData): #writes to mutes.txt
        with open(TEXT_FILES / 'mutelog.txt', 'w', encoding='utf-8') as f:
            json.dump(cData, f, indent=4)
            #w or w+ overwrites previous data
            #a or a+ appends data but gives JSONDecodeError

    def ReadBlyat(self): #reads mutes.txt
        Path(TEXT_FILES / 'mutelog.txt').touch(exist_ok=True)
        #if Path(TEXT_FILES / 'mutelog.txt').stat().st_size <= 2:
        #    raise NeedInstallFirst
        with open(TEXT_FILES / 'mutelog.txt', 'r') as f:
            return json.load(f)


#--------S1, START OF DATA COLLECTION AND LOGGING
    def TimeBlyat(self, MT2: int): #gets time of mute from mutes.txt
        content = self.ReadBlyat()

        get_time = [content[i]['timeMute']
                        for i in content if content[i]['timeMute'] == MT2]

        if get_time:
            return get_time[0]
        return None


    def MutesBlyat(self, MUTE: int): #get mute time from mutes.txt
        content = self.ReadBlyat()

        get_mute = [content[i]['muteTime']
                        for i in content if content[i]['muteTime'] == MUTE]

        if get_mute:
            return get_mute[0]
        return None


    def MemberBlyat(self, MEMBER: int): #get member id from mutes.txt
        content = self.ReadBlyat()

        get_member = [content[i]['memberID']
                        for i in content if content[i]['memberID'] == MEMBER]

        if get_member:
            return get_member[0]
        return None


    def ServerBlyat(self, ctx, SERVER: int):
        content = self.ReadBlyat()

        get_server = [content[i]['serverID']
                        for i in content if content[i]['serverID'] == SERVER]

        if get_server:
            return get_server[0]
        else:
            return None


    def RolesBlyat(self, ctx, ROLES1: list, member: discord.Member = None): #gets roles of a user before mute
        if ROLES1:
            #ROLES2 = list(role for role in member.roles if role.name != '@everyone')
            print(ROLES1)

            content = self.ReadBlyat()

            get_roles = [content[i]['userRoles']
                            for i in content if content[i]['userRoles'] == get_roles]

            if get_roles:
                return get_roles
        else:
            return get_roles


    def UpdateBlyat(self, MUTE, MEMBER, SERVER, ROLES1, MT2) -> None: #updates mutes.txt
        Path(TEXT_FILES / 'mutelog.txt').touch(exist_ok=True)

        #print("Json Size:", Path(TEXT_FILES / 'mutelog.txt').stat().st_size)
        if Path(TEXT_FILES / 'mutelog.txt').stat().st_size <= 4:
            print("hello")
            cData = {
                0: {
                    'serverID': SERVER,
                    'memberID': MEMBER,
                    'muteTime': MUTE,
                    'userRoles': ROLES1,
                    'timeMute': MT2
                }
            }
            self.WriteBlyat(cData)
            return
        else:
            content = self.ReadBlyat()
            for key in list(content.keys()):
                checkmem = [content[i]['memberID'] for i in content if content[i]['memberID'] == MEMBER and content[i]['serverID'] == SERVER]
                if not checkmem:
                    print(content[key]['memberID'])
                    print(len(content.keys()))
                    KAX = len(content.keys())
                    cData = {
                        KAX+1: {
                            'serverID': SERVER,
                            'memberID': MEMBER,
                            'muteTime': MUTE,
                            'userRoles': ROLES1,
                            'timeMute': MT2
                        }
                    }
                    content.update(cData)
                    self.WriteBlyat(content)
                    return

                else:
                    return


    def EraseBlyat(self, Mx, Gx): #unmute/removes a specified block
        with open(TEXT_FILES / 'mutelog.txt', 'r') as f:
            com = json.load(f)
        for key in list(com.keys()):
            if com[key]['memberID'] == Mx and com[key]['serverID'] == Gx:
                del com[key]
                self.WriteBlyat(com)
                return True
            #else:
            #    return False

#--------S1, END OF DATA COLLECTION AND LOGGING

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *,Time:ConvertBlyat = None):
        if Time is not None:
            # PRE-MUTE: ESTABLISH VARIABLES & EXCEPTIONS
            mr = discord.utils.get(ctx.guild.roles, name='muted')
            MT2 = TimeNahui2()
            MUTE = Time #FOR MUTES.TXT
            MEMBER = member.id #FOR MUTES.TXT
            SERVER = ctx.guild.id #FOR MUTES.TXT
            CHANNELC = ctx.channel.id
            ROLES1 = tuple(role.id for role in member.roles if role.name != '@everyone') #FOR MUTES.TXT / Convienence
            CHANNELS = (channel.id for channel in ctx.guild.channels)

            if mr in member.roles:
                await ctx.send("That member has already been muted!")
                return

            try:
                MC = self.ChannelMod(ctx.guild.id)
                print(MC)
            except NeedInstallFirst:
                print("Mod channel not set up")


            #BLYAT = (MUTE, MEMBER, SERVER, ROLES1)
            print("1")
            if member.id == ctx.author.id:
                return
            #if member.id == HF:
            #    return

            if not mr:
                try: #if no muted role found, create one and carry on
                    guild = ctx.guild
                    perms_nppb = discord.Permissions(send_messages=False, read_messages=True)
                    mr = await ctx.guild.create_role(name='muted', permissions=perms_nppb)
                    await ctx.send("No `muted` role found, so I created one!")

                except discord.ext.commands.errors.BotMissingPermissions:
                    await ctx.send("I need `manage_roles` perms")
                    return

            print("3")
            ROLES2 = [role for role in member.roles if role.name != '@everyone']
            for role in ROLES2:
                await member.remove_roles(role)
            #print("{}, Roles removed".format(member)) #removes user's roles

            await member.add_roles(mr)
            A2 = self.UpdateBlyat(MUTE, MEMBER, SERVER, ROLES1, MT2) #sends data to file
            print("Updated!")
            A3 = self.MutesBlyat(MUTE) #get mute duration from mutes.txt (integer)
            print("Mute:", A3)
            A4 = self.MemberBlyat(MEMBER) #get member from mutes.txt ()
            print("Member:", A4)
            A5 = self.ServerBlyat(ctx, SERVER) #get server from mutes.txt
            print("Server:", A5)
            A6 = self.ChannelMod(SERVER)
            print("Mod Channel:", A6)
            A7 = self.TimeBlyat(MT2)
            print("Time of Mute:", A7)
            print(MEMBER, "added to file")

            await ctx.send(":mute: `{} has been muted by {} for {} seconds`".format(member.name, ctx.author.name, MUTE))

            if MC is not None:
                chaz = (discord.utils.get(ctx.guild.channels, id=MC) for channel in CHANNELS)
                for channel in chaz:
                    embed = discord.Embed(
                        title='***DIGITAL ANIMAL***\n*Moderation*',
                        description='*Member Muted*',
                        color=discord.Colour.random()
                        )
                    embed.set_thumbnail(url=member.avatar.url)
                    embed.set_footer(text=f'Time: {TimeNahui()}')
                    embed.add_field(name=f'`{ctx.author.name} muted {str(member)}`', value=f'`Duration: {MUTE} seconds`', inline=False)
                    #embed.add_field(name=f'`Projected time of unmute:`', value='{}'.format(XY), inline=False)
                    await channel.send(embed=embed)
                    return
            else:
                pass

        else:
            await ctx.send("`You must include a time (#s,#m,#h,#d)`")
            return





    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send("`Missing permissions, must have manage_roles perms")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("`You must @mention a user`")
            return


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, rez = None):
            mr = discord.utils.get(ctx.guild.roles, name='muted')
            Roles = tuple(role.id for role in member.roles if role.name != '@everyone')
            if len(member.roles) is not None: #if member has role(s)
                Roles2 = (role for role in member.roles if role.name != '@everyone')
                for role in Roles2:
                    await member.remove_roles(role)
                    print(member, "removed mute role")
                    #await ctx.send("`{} has been unmuted`\nYou will need to manually add their roles back".format(member.name))
                    content = self.ReadBlyat()
                    for key, value in list(content.items()):
                        X = (value['userRoles'])
                        Y = (value['memberID'])
                        Z = (value['serverID'])
                        restore = (discord.utils.get(member.guild.roles, id=role) for role in value['userRoles'])
                        for role in restore:
                            try:
                                print(role)
                                await member.add_roles(role)
                                print(f"{member.name} unmuted, roles removed")
                                self.EraseBlyat(member.id, Z)
                                print(f'{member.name} removed from file')
                            except Exception:
                                await ctx.send(Exception)
                                return
            else:
                return

            try:
                C1 = (channel.id for channel in ctx.guild.channels)
                MC = self.ChannelMod(ctx.guild.id)
                #print(MC)
            except NeedInstallFirst:
                print("Mod channel not set up")
                return None

            if MC is not None:
                chaz = (discord.utils.get(ctx.guild.channels, id=MC) for channel in C1)
                for channel in chaz:

                    embed = discord.Embed(
                        title='***DIGITAL ANIMAL***\n*Moderation*',
                        description='*Member Unmuted*',
                        color=discord.Colour.random()
                        )
                    embed.set_thumbnail(url=member.avatar.url)
                    embed.set_footer(text=f'Time: {TimeNahui()}')
                    embed.add_field(name=f'`{ctx.author.name} unmuted {str(member)}`', value=f'`Reason: {rez}`', inline=False)

                    await channel.send(embed=embed)
                    return
            else:
                pass

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send("`Missing permissions, must have manage_roles perms`")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("`You must @mention a user`")
            return


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, number: int):
        await ctx.channel.purge(limit=number)
        try:
            C1 = (channel.id for channel in ctx.guild.channels)
            MC = self.ChannelMod(ctx.guild.id)
            print(MC)
        except NeedInstallFirst:
            print("Mod channel not set up")
            return None

        if MC is not None:
            chaz = (discord.utils.get(ctx.guild.channels, id=MC) for channel in C1)
            for channel in chaz:
                print(channel)

                embed = discord.Embed(
                    title='***DIGITAL ANIMAL***\n*Moderation*',
                    description='*Messages Cleared*',
                    color=discord.Colour.random()
                    )
                embed.set_thumbnail(url=ctx.author.avatar.url)
                embed.set_footer(text=f'Time: {TimeNahui()}')
                embed.add_field(name=f'`{ctx.author.name} cleared messages`', value=f'`Count: {number}`', inline=False)

                await channel.send(embed=embed)
                return
        else:
            pass

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send("`Missing permissions, you must be have manage_messages permission`")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("`You must @mention a user`")
            return


    @commands.command(aliases=['jail'])
    @commands.has_permissions(manage_roles=True)
    async def timeout(self, ctx, member: discord.Member=None, reason=None):
        if not member:
            await ctx.send("`You must @mention the user you are trying to imprison`")
            return
        elif member.bot:
            await ctx.send("no")
            return
        else:
            def get_prisoner_role(self):
                prisoner_role = discord.utils.get(ctx.guild.roles, name='prisoner')
                return prisoner_role

            def get_prisoner_channel(self):
                prisoner_channel = discord.utils.get(ctx.guild.text_channels, name='jail')
                return prisoner_channel
            # create prisoner ROLE

            if get_prisoner_role(self) is None:
                await ctx.guild.create_role(name='prisoner', color=discord.Colour(0x090909))
            # create prisoner CHANNEL

            if get_prisoner_channel(self) is None:
                await ctx.guild.create_text_channel(name='jail')
            # permissions for other channels -> except gulag prison
            overwrite = discord.PermissionOverwrite()
            overwrite.view_channel = False
            all_channels = [channel for channel in ctx.guild.text_channels if channel.name != 'jail']

            for channel in all_channels:
                await channel.set_permissions(get_prisoner_role(self), overwrite=overwrite)

            # permissions for everyone to gulag prison
            everyone_role = discord.utils.get(ctx.guild.roles, name='@everyone')

            for_all = discord.PermissionOverwrite()
            for_all.view_channel = False

            role_gulag = discord.PermissionOverwrite()
            role_gulag.view_channel = True

            await get_prisoner_channel(self).set_permissions(everyone_role, overwrite=for_all)
            await get_prisoner_channel(self).set_permissions(get_prisoner_role(self), overwrite=role_gulag)

            # remove roles from member and giving the role gulag
            roles_member = [role for role in member.roles if role.name != '@everyone']
            for role in roles_member:
                try:
                    await member.remove_roles(role)
                except Exception as e:
                    print(e)
                    continue

            await member.add_roles(get_prisoner_role(self))
            await ctx.send("Jailed")

            try:
                C1 = (channel.id for channel in ctx.guild.channels)
                MC = self.ChannelMod(ctx.guild.id)
                print(MC)
            except NeedInstallFirst:
                print("Mod channel not set up")
                return None

            if MC is not None:
                chaz = (discord.utils.get(ctx.guild.channels, id=MC) for channel in C1)
                for channel in chaz:
                    print(channel)

                    embed = discord.Embed(
                        title='***DIGITAL ANIMAL***\n*Moderation*',
                        description='*Someone just went to jail!*',
                        color=discord.Colour.random()
                        )
                    embed.set_thumbnail(url=member.avatar.url)
                    embed.set_footer(text=f'Time: {TimeNahui()}')
                    embed.add_field(name=f'`{str(member)} Went to Jail`', value=f'`Reason : {reason}`', inline=False)
                    await channel.send(embed=embed)
                    return
            else:
                pass

    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send("`Missing permissions, must have manage_roles perms`")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("`You must @mention a user`")
            return


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def free(self, ctx, member: discord.Member, reason=None):
        gulag_prison = discord.utils.get(ctx.guild.roles, name="prisoner")
        await member.remove_roles(gulag_prison)
        await ctx.send(f"Freed {member.name}")
        try:
            C1 = (channel.id for channel in ctx.guild.channels)
            MC = self.ChannelMod(ctx.guild.id)
            print(MC)
        except NeedInstallFirst:
            print("Mod channel not set up")
            return None

        if MC is not None:
            chaz = (discord.utils.get(ctx.guild.channels, id=MC) for channel in C1)
            for channel in chaz:
                print(channel)

                embed = discord.Embed(
                    title='***DIGITAL ANIMAL***\n*Moderation*',
                    description='*Freedom*',
                    color=discord.Colour.random()
                    )
                embed.set_thumbnail(url=ctx.author.avatar.url)
                embed.set_footer(text=f'Time: {TimeNahui()}')
                embed.add_field(name=f'`{str(member)} has been freed from Jail`', value=f'`Reason: {reason}`' ,inline=False)

                await channel.send(embed=embed)
                return
        else:
            pass

    @free.error
    async def free_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send("`Missing permissions, must have manage_roles perms`")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("`You must @mention a user`")
            return


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx):
        await ctx.channel.purge(limit=1000000)

    @nuke.error
    async def nuke_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send("`Not so fast! :p`")
            return


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, reason=None):
        if not member:
            await ctx.send("`You must @mention the user you are trying to kick`")
            return
        #if member.id == HF:
        #    return
        elif member.id == ctx.author.id:
            return
        try:
            await member.kick()
            try:
                C1 = (channel.id for channel in ctx.guild.channels)
                MC = self.ChannelMod(ctx.guild.id)
                print(MC)
            except NeedInstallFirst:
                print("Mod channel not set up")
                return None

            if MC is not None:
                chaz = (discord.utils.get(ctx.guild.channels, id=MC) for channel in C1)
                for channel in chaz:
                    print(channel)

                    embed = discord.Embed(
                        title='***DIGITAL ANIMAL***\n*Moderation*',
                        description='*Member Kicked!*',
                        color=discord.Colour.random()
                        )
                    embed.set_thumbnail(url=ctx.author.avatar.url)
                    embed.set_footer(text=f'Time: {TimeNahui()}')
                    embed.add_field(name=f'`{ctx.author.name} kicked {str(member)} from the server`', value=f'`Reason: {reason}`', inline=False)

                    await channel.send(embed=embed)
                    return
            else:
                await ctx.send("Kicked")
                pass

        except discord.ext.commands.errors.BotMissingPermissions:
            await ctx.send("I do not have permission to do that, I need admin!")
            return

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send("`Missing permissions, must have kick_members perms`")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("`You must @mention a user`")
            return


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, reason=None):
        if not member:
            await ctx.send("`You must @mention the user you are trying to ban`")
            return
        elif member.id == ctx.author.id:
            return
        try:
            await member.ban()
            await ctx.send(":hammer: `{} was banned by {}`".format(member.name, ctx.author.name))
            try:
                C1 = (channel.id for channel in ctx.guild.channels)
                MC = self.ChannelMod(ctx.guild.id)
                print(MC)
            except NeedInstallFirst:
                print("Mod channel not set up")
                return None

            if MC is not None:
                chaz = (discord.utils.get(ctx.guild.channels, id=MC) for channel in C1)
                for channel in chaz:
                    print(channel)

                    embed = discord.Embed(
                        title='***DIGITAL ANIMAL***\n*Moderation*',
                        description='*Member BANNED*',
                        color=discord.Colour.random()
                        )
                    embed.set_thumbnail(url=member.avatar.url)
                    embed.set_footer(text=f'Time: {TimeNahui()}')
                    embed.add_field(name=f'`{member.name} just got FUCKING BANNED!`', value=f"`Reason: {reason}`", inline=False)

                    await channel.send(embed=embed)
                    return
            else:
                pass

        except Exception as e:
            await ctx.send(e)
            return

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send("`Missing permissions, must have ban_members perms`")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("`You must @mention a user`")
            return


    @commands.command() #fix
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member, reason=None):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
            try:
                C1 = (channel.id for channel in ctx.guild.channels)
                MC = self.ChannelMod(ctx.guild.id)
                print(MC)
            except NeedInstallFirst:
                print("Mod channel not set up")
                return None

            if MC is not None:
                chaz = (discord.utils.get(ctx.guild.channels, id=MC) for channel in C1)
                for channel in chaz:
                    print(channel)

                    embed = discord.Embed(
                        title='***DIGITAL ANIMAL***\n*Moderation*',
                        description='*Member UNBANNED*',
                        color=discord.Colour.random()
                        )
                    embed.set_thumbnail(url=ctx.member.avatar.url)
                    embed.set_footer(text=f'Time: {TimeNahui()}')
                    embed.add_field(name=f'`{ctx.author.name} unbanned {ctx.member}`', value=f"Reason: {reason}", inline=False)

                    await chaz.send(embed=embed)
                    return
            else:
                pass


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member=None, *,reason=None):
        if not member:
            await ctx.send("`You must @mention the user you are trying to warn`")
            return
        if member.id == HF:
            return
        elif member.id == ctx.author.id:
            return

        try:
            await ctx.channel.purge(limit=1)

            embed = discord.Embed(
                    description=f'You have been warned in `{ctx.guild}`\n{reason}\nAt: {datetime.now().strftime("%H:%M:%S")}',
                    colour=discord.Color.random()
                )
            dmw = await member.create_dm()
            await dmw.send(embed=embed)
            try:
                C1 = (channel.id for channel in ctx.guild.channels)
                MC = self.ChannelMod(ctx.guild.id)
                print(MC)
            except NeedInstallFirst:
                print("Mod channel not set up")
                return None

            if MC is not None:
                chaz = (discord.utils.get(ctx.guild.channels, id=MC) for channel in C1)
                for channel in chaz:
                    print(channel)

                embed = discord.Embed(
                    title='***DIGITAL ANIMAL***\n*Moderation*',
                    description='*Member Warned*',
                    color=discord.Colour.random()
                    )
                embed.set_thumbnail(url=member.avatar.url)
                embed.set_footer(text=f'Time: {TimeNahui()}')
                embed.add_field(name=f'`{ctx.author.name} warned {member}`', value=f"`Reason: {reason}`", inline=False)

                await channel.send(embed=embed)
                return
            else:
                pass

        except discord.ext.commands.errors.BotMissingPermissions:
            await ctx.send("I do not have permission to do that, I need admin!")
            return

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send("`Missing permissions, must have manage_messages perms`")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("`You must @mention a user`")
            return


    @commands.command()
    #@commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member=None, *,role: discord.Role=None):
        if not member:
            await ctx.send("`You must @mention the user you are trying to addrole`")
            return
        if not role:
            await ctx.send("`You must pass in @role for it to work`")
            return
        if role in ctx.guild.roles:
            await member.add_roles(role)
            return
        else:
            await ctx.send("`That role does not exist`")
            return

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send("`Missing permissions, must have manage_roles perms`")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("`You must @mention a user`")
            return

        


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def delrole(self, ctx, member: discord.Member=None, *,role: discord.Role=None):
        if not member:
            await ctx.send("`You must @mention the user you are trying to delrole`")
            return
        if not role:
            await ctx.send("`You must pass in @role for it to work`")
            return
        if role in member.roles:
            await member.remove_roles(role)
            return
        else:
            await ctx.send("That role does not exist")
            return

    @unmute.error
    async def delrole_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send("`Missing permissions, must have manage_roles perms`")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("`You must @mention a user`")
            return


    @commands.command()
    async def dm(self, ctx, user: discord.Member, *, message=None):
        AZU = [273255595509809162, 773695202136686612]
        for uz in AZU:
            if ctx.author.id in AZU:
                await ctx.channel.purge(limit=1)

                embed = discord.Embed(
                        description=message,
                        colour=discord.Color.random()
                    )

                channel = await user.create_dm()
                await channel.send(embed=embed)
                channel = client.get_channel(699655178818814013)
                embed = discord.Embed(
                        title='Direct Message Log',
                        description=f'Message: `{message}`\nAuthor: `{ctx.author}`\nRecipient: `{user}`',
                        color=discord.Colour.random()
                    )
                await channel.send(embed=embed)
            else:
                return




async def setup(client):
    await client.add_cog(Admin_Commands(client))
