import discord
from discord.ext import commands
from blagues_api import BlaguesAPI
import asyncio

allowed_channels = [796137851972485151, 697492398070300763, 796731890630787126, 631935311592554636] #["🤖・cow-bip-bop-bots", "bruh-botsandmusic", "test-bot", "général de mon propre serveur"]

def checks_in_bot_channel(channels, channel):
    global allowed_channels
    for i in range(len(allowed_channels)):
        channel_id = allowed_channels[i]
        print(channel_id, channel)
        if channel_id == channel:
            return True
    return False

class CogOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def blague(self, ctx):
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel):
            with open('token_blague.txt', 'r') as token_blague:
                blagues = BlaguesAPI(str(token_blague))
            
            async def show():
                return await blagues.random()

            await show()
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")
