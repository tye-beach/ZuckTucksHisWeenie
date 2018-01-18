import discord
import utils.data as data
from utils.roles import get_role, get_next_role, roles
from discord.ext import commands
import asyncio
from utils.data import joined


class RolesConfig:

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def remove_roles(self, ctx):
        """This command removes ALL the roles ranking"""
        roles.clear()
        await self.bot.say('Role ranking removed!')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def add_role(self, ctx, role_name: str, invites_needed: int):
        """<role-name><invites-needed>"""
        roles[invites_needed] = role_name
        await self.bot.say('Affiliate Role added to Ranking! Type !rank for seeing it')


def setup(bot: commands.Bot):
    bot.add_cog(RolesConfig(bot))
