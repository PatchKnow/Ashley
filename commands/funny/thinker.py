from discord.ext import commands
from random import choice
from resources.db import Database
from resources.ia_list import pensador
from resources.check import check_it


class Thinkers(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='thinker', aliases=['pensador'])
    async def thinker(self, ctx):
        answer = choice(pensador)
        await ctx.message.channel.send("Assim diz o **pensador**: ``{}``".format(answer))


def setup(bot):
    bot.add_cog(Thinkers(bot))
    print('\033[1;32mO comando \033[1;34mPENSADOR\033[1;32m foi carregado com sucesso!\33[m')
