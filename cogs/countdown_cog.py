import utils.data as data
from discord.ext import commands
from datetime import datetime, timedelta
import discord
import asyncio


class CountdownCommands:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.countdown = None
        self.bot.loop.create_task(self.changy())

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def set_countdown(self, ctx, hours: int, minutes: int=0):
        """<hours> sets a countdown"""
        now = datetime.now() + timedelta(hours=hours, minutes=minutes)
        self.countdown = now
        await self.bot.say('Countdown set!')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def set_countdown_event(self, ctx, date):
        """<hh:MM dd-mm-YY> sets a countdown"""
        self.countdown = datetime.strptime(date, '%H:%M %d-%m-%Y')
        await self.bot.say('Countdown set!')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def cancel_countdown(self):
        """Cancels current countdown"""
        self.countdown = None
        await self.bot.say('Countdown canceled!')

    @commands.command(pass_context=True)
    async def event(self):
        """Shows the current countdown"""
        if self.countdown is None:
            await self.bot.say('There is no event scheduled... ')
            return
        now = datetime.now()
        time_left = self.countdown - now
        days, seconds = time_left.days, time_left.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        await self.bot.say('```python\n {} hours {} minutes {} seconds until next pump!```'.format(hours, minutes, seconds))

    async def changy(self):
        while not self.bot.is_closed:
            await asyncio.sleep(10)
            if self.countdown is None:
                continue
            print('Updating time...')
            now = datetime.now()
            time_left = self.countdown - now
            days, seconds = time_left.days, time_left.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            await self.bot.change_presence(game=discord.Game(name='pump in {}d {}:{}'.format(days, hours, minutes)))


def setup(bot: commands.Bot):
    bot.add_cog(CountdownCommands(bot))
