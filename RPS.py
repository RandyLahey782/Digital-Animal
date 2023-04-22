import discord
from discord.ext import commands
import random
from random import randint
from random import choice as randchoice
import datetime
import time
import aiohttp
import asyncio




class RockPaperScissors(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def rps(self, ctx, rps: str):
        x1 = "`k rps [rock or paper or scissors]` "
        kr = ['rock', 'paper', 'scissors']

        kr2 = random.choice(kr)
        if rps == 'rock':
            print(kr2)
            if kr2 == 'rock':
                print(rps, kr2)
                await ctx.send("*Ah man! We tied!*\nYour choice: `{}`\nOur choice: `{}`".format(rps, kr2))
                return
            elif kr2 == 'scissors':
                print(rps, kr2)
                await ctx.send("*You devil!*")
                return
            elif kr2 == 'paper':
                print(rps, kr2)
                await ctx.send("*Paper beats rock*\n`Digital Animal` beats `{}`".format(ctx.author.name))
                return


        elif rps == 'scissors':
            print(kr2)
            if kr2 == 'scissors':
                print(rps, kr2)
                await ctx.send("*Ah crap! We tied!*\nYour choice: `{}`\nOur choice: `{}`".format(rps, kr2))
                return
            elif kr2 == 'rock':
                print(rps, kr2)
                await ctx.send('*Rock beats scissors*\nDigital Animal beats `{}`'.format(ctx.author.name))
                return
            elif kr2 == 'paper':
                print(rps, kr2)
                await ctx.send("*noob, you beat me!*")
                return


        elif rps == 'paper':
            print(kr2)
            if kr2 == 'paper':
                print(rps, kr2)
                await ctx.send("Doggonit We tied!\nYour choice: `{}`\nOur choice: `{}`".format(rps, kr2))
                return
            elif kr2 == 'scissors':
                print(rps, kr2)
                await ctx.send("*Scissors beat paper*\n`Digital Animal` beats `{}`".format(ctx.author.name))
                return
            elif kr2 == 'rock':
                print(rps, kr2)
                await ctx.send("*you cheated!*")
                return


        else:
            await ctx.send("rock, paper, or scissors")
            return


async def setup(client):
    await client.add_cog(RockPaperScissors(client))
