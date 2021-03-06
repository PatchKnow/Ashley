import json
import discord

from random import choice

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)

gif = ['https://media.giphy.com/media/bAmQn1R4V3owE/giphy.gif',
       'https://media.giphy.com/media/skVEP0BeduG4/giphy.gif',
       'https://media.giphy.com/media/3o7TKsJEd0lp7GNUpq/giphy.gif',
       'https://media.giphy.com/media/138CCLzEja7I3e/giphy.gif',
       'https://media.giphy.com/media/l3V0uEmPgKpjZH6ve/giphy.gif',
       'https://media.giphy.com/media/nRPxv0FVLQBJm/giphy.gif',
       'https://media.giphy.com/media/papraODOQ51yE/giphy.gif',
       'https://media.giphy.com/media/GncBDxr7YxsuQ/giphy.gif',
       'https://media.giphy.com/media/3ZZeiFwplAGlLxHNvQ/giphy.gif',
       'https://media.giphy.com/media/lq2WK9kzLTLos/giphy.gif']


class OnMemberJoin(object):
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):

        data = self.bot.db.get_data("guild_id", member.guild.id, "guilds")
        if data is not None:

            if data['func_config']['member_join']:
                try:
                    if member.guild.system_channel is not None:
                        to_send = discord.Embed(
                            title="SEJA MUITO BEM VINDO AO SERVIDOR {}:".format(member.guild),
                            color=color,
                            description="{}, Eu sou o BOT oficial do(a) {}, qualquer coisa "
                                        "digite ``ash.ajuda`` que eu irei ajudar você com "
                                        "muito prazer!".format(member.name, member.guild))
                        to_send.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                        to_send.set_thumbnail(url="{}".format(member.avatar_url))
                        to_send.set_image(url=choice(gif))
                        to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                        await member.guild.system_channel.send(embed=to_send)
                    else:
                        to_send = discord.Embed(
                            title="SEJA MUITO BEM VINDO AO SERVIDOR {}:".format(member.guild),
                            color=color,
                            description="{}, Eu sou o BOT oficial do(a) {}, qualquer coisa "
                                        "digite ``ash.ajuda`` que eu irei ajudar você com "
                                        "muito prazer!".format(member.name, member.guild))
                        to_send.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                        to_send.set_thumbnail(url="{}".format(member.avatar_url))
                        to_send.set_image(url=choice(gif))
                        to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                        channel_ = self.bot.get_channel(data['func_config']['member_join_id'])
                        await channel_.send(embed=to_send)
                except discord.errors.Forbidden:
                    pass
                except AttributeError:
                    pass

            if data['func_config']['cont_users']:
                numbers = ['0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
                channel_ = self.bot.get_channel(data['func_config']['cont_users_id'])
                if channel_ is None:
                    return
                text = str(member.guild.member_count)
                for n in range(0, 10):
                    text = text.replace(str(n), numbers[n])
                await channel_.edit(topic="Membros: " + text)

            if _auth['default_guild'] == member.guild.id:
                role = discord.utils.find(lambda r: r.name == "</Members>", member.guild.roles)
                await member.add_roles(role)
                channel_ = self.bot.get_channel(data['func_config']['member_join_id'])
                embed = discord.Embed(
                    color=color,
                    description="<a:blue:525032762256785409>│``USE O COMANDO`` **ash cargos** ``PARA VOCE VER OS "
                                "CARGOS DISPONIVEIS``")
                await channel_.send(embed=embed)


def setup(bot):
    bot.add_cog(OnMemberJoin(bot))
    print('\033[1;32mO evento \033[1;34mMEMBER_JOIN\033[1;32m foi carregado com sucesso!\33[m')
