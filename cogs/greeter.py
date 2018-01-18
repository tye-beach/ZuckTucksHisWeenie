from discord.ext import commands
import discord
import asyncio
import utils.data


class Greeter:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def on_member_join(self, member: discord.Member):
        # Greetings	
        welcome_channel = self.bot.get_channel('391629660905013250')
        await self.bot.send_message(welcome_channel, 'Welcome to our discord server, {}!'.format(member.mention))


def setup(bot: commands.Bot):
    bot.add_cog(Greeter(bot))
