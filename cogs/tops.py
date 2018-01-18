import discord
import utils.data as data
from utils.roles import get_role, get_next_role, get_previous_role, roles
from discord.ext import commands
import discord.errors
import asyncio


class Tops:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True, name='top10')
    @commands.has_permissions(manage_server=True)
    async def top_inviters(self, ctx):
        # List of tuples of users and their invites like [user, invites_number]
        users_tuple = data.users_invites.values()

        # Sorts by number of invites (position 1)
        def top_sorter(item):
            return item[1]

        top_10_users = sorted(users_tuple, key=top_sorter, reverse=True)[:10]

        message = '**Top 10 Members (In order from most invited to least)\n**'
        count = 1
        for top_user in top_10_users:
            message += '{}: {} has {} invites\n'.format(count, top_user[0].mention, top_user[1])
            count += 1
        await self.bot.say(message)


def setup(bot: commands.Bot):
    bot.add_cog(Tops(bot))

