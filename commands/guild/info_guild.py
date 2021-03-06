import json
import discord
import datetime

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class ServerInfo(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='serverinfo', aliases=['infoserver'])
    async def serverinfo(self, ctx):
        hour = datetime.datetime.now().strftime("%H:%M:%S")
        embed = discord.Embed(title="\n", color=color, description="Abaixo está as informaçoes principais do servidor!")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text="{} • {}".format(ctx.author, hour))
        embed.add_field(name="Nome:", value=ctx.guild.name, inline=True)
        embed.add_field(name="Dono:", value=ctx.guild.owner.mention)
        embed.add_field(name="ID:", value=ctx.guild.id, inline=True)
        embed.add_field(name="Cargos:", value=str(len(ctx.guild.roles)), inline=True)
        embed.add_field(name="Membros:", value=str(len(ctx.guild.members)), inline=True)
        embed.add_field(name="Bots:", value=str(len([a for a in ctx.guild.members if a.bot])), inline=True)
        embed.add_field(name="Criado em:", value=ctx.guild.created_at.strftime("%d %b %Y %H:%M"), inline=True)
        embed.add_field(name="Região:", value=str(ctx.guild.region).title(), inline=True)
        embed.add_field(name="Comandos Usados: ", value=str(self.bot.guilds_commands[ctx.guild.id]), inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ServerInfo(bot))
    print('\033[1;32mO comando \033[1;34mSERVERINFO\033[1;32m foi carregado com sucesso!\33[m')
