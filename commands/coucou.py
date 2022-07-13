import discord
from discord.ext import commands

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
    async def coucou(self, ctx, member):
        current_channel = ctx.message.channel.id
        channels = ctx.guild.channels
        if checks_in_bot_channel(channels, current_channel) == True:
            if {ctx.author.mention} == member:
                ctx.send("T'es teubé ou quoi ? Tu peux pas te faire coucou à toi-même ?! Y a que toi pour être si teubé que ça !!")
            else:
                if member == "@everyone":
                    member = "tout le monde"
                coucous = ["https://i.gifer.com/6ZFR.gif", "https://i.gifer.com/1UEW.gif", "https://i.gifer.com/UUP.gif", "https://i.gifer.com/Wx6B.gif", "https://i.gifer.com/WShb.gif", "https://i.gifer.com/1rO6.gif", "https://i.gifer.com/5Tz.gif", "https://i.gifer.com/CMSH.gif"]
                coocky = coucous[randint(0,len(coucous)-1)]
                emb = discord.Embed(title=None, description = f"{ctx.author.mention} fait un coucou à {member}", color=0x3498db)
                emb.set_image(url=f"{coocky}")
                await ctx.send( embed = emb)
        else:
            await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur)
