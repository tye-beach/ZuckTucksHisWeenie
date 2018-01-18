import utils.data as data
from discord.ext import commands
import discord


class SpamDeleter:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.countdown = None

    async def on_message(self, message: discord.Message):
        try:
            if 'https://discord.gg/' in message.content:
                await self.bot.delete_message(message)
                await self.bot.kick(message.author)
                await self.bot.send_message(message.author, 'You cannot share other invites!')
        except:
            pass


def setup(bot: commands.Bot):
    bot.add_cog(SpamDeleter(bot))
