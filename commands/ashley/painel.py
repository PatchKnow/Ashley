import json
import discord

from discord.ext import commands
from asyncio import sleep
from resources.translation import t_
from resources.check import check_it
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)

_list = ['</Shop>', '</Lore>']

msg_id = None
msg_user = None


class Panel(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='roles', aliases=['cargos'])
    async def roles(self, ctx):
        if ctx.guild.id == _auth['default_guild']:
            embed = discord.Embed(
                title="Escolha a área que você deseja ver:",
                color=color,
                description="- Para pegar o cargo **</Shop>**: Clique em :skull_crossbones:\n"
                            "- Para pegar o cargo **</Lore>**: Clique em :crossed_swords:\n")
            bot_msg = await ctx.send(embed=embed)
            await bot_msg.add_reaction('☠')
            await bot_msg.add_reaction('⚔')
            global msg_id
            msg_id = bot_msg.id
            global msg_user
            msg_user = ctx.author
        else:
            await ctx.send(
                t_(ctx, "<:negate:520418505993093130>│``Desculpe, mas apenas os`` **Membros do meu servidor** ``podem "
                        "usar esse comando!``", "guilds"))

    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return

        global timer

        msg = reaction.message
        timer = True

        if reaction.emoji == "☠" and msg.id == msg_id and user == msg_user:
            if timer:
                timer = False
                rules = [r.name for r in user.roles]
                for c in range(0, len(rules)):
                    if rules[c] in _list:
                        role = discord.utils.find(lambda r: r.name == rules[c], msg.guild.roles)
                        await user.remove_roles(role)
                        await sleep(1)
                role = discord.utils.find(lambda r: r.name == "</Shop>", msg.guild.roles)
                await user.add_roles(role)
                await sleep(1)
                timer = True

        if reaction.emoji == "⚔" and msg.id == msg_id and user == msg_user:
            if timer:
                timer = False
                rules = [r.name for r in user.roles]
                for c in range(0, len(rules)):
                    if rules[c] in _list:
                        role = discord.utils.find(lambda r: r.name == rules[c], msg.guild.roles)
                        await user.remove_roles(role)
                        await sleep(1)
                role = discord.utils.find(lambda r: r.name == "</Lore>", msg.guild.roles)
                await user.add_roles(role)
                await sleep(1)
                timer = True

    async def on_reaction_remove(self, reaction, user):
        if user.id == self.bot.user.id:
            return

        msg = reaction.message

        if reaction.emoji == "☠" and msg.id == msg_id and user == msg_user:
            rules = [r.name for r in user.roles]
            for c in range(0, len(rules)):
                if rules[c] in _list:
                    role = discord.utils.find(lambda r: r.name == rules[c], msg.guild.roles)
                    await user.remove_roles(role)
                    await sleep(1)

        if reaction.emoji == "⚔" and msg.id == msg_id and user == msg_user:
            rules = [r.name for r in user.roles]
            for c in range(0, len(rules)):
                if rules[c] in _list:
                    role = discord.utils.find(lambda r: r.name == rules[c], msg.guild.roles)
                    await user.remove_roles(role)
                    await sleep(1)


def setup(bot):
    bot.add_cog(Panel(bot))
    print('\033[1;32mO comando \033[1;34mPAINEL\033[1;32m foi carregado com sucesso!\33[m')
