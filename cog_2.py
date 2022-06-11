import discord
from discord.ext import commands

class CogOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wesh(self, ctx):
        await ctx.send("coucou")
