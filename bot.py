import sys
import os
import traceback
import discord
from discord.ext import commands
import utils.data as data
import utils.roles

print Tye Beach

description = '''Aventus Bot'''

modules = {'cogs.roles_management', 'cogs.secret_channel', 'cogs.roles_config', 'cogs.countdown_cog',
           'cogs.cleaner', 'cogs.greeter', 'cogs.tops', 'cogs.spam_deleter'}

bot = commands.Bot(command_prefix='!', description=description)


@bot.event
async def on_ready():
    print('Aventus Bot starting...')

    print(bot.user.name)
    print(bot.user.id)
    data.server = bot.get_server('391626662351077386')
    members = data.server.members
    online_members = list(filter(lambda x: not x.status == discord.Status.offline, members))
    await bot.change_presence(
        game=discord.Game(name='with {}/{} Members!'.format(online_members.__len__(), data.server.members.__len__())))
    print('Loading cogs...')
    if __name__ == '__main__':
        modules_loaded = 0
        for module in modules:
            try:
                bot.load_extension(module)
                print('\t' + module)
                modules_loaded += 1
            except Exception as e:
                traceback.print_exc()
                print('Error loading the extension {module}', file=sys.stderr)
        print(str(modules_loaded) + '/' + str(modules.__len__()) + ' modules loaded')
        print('Systems 100%')
        print(data.server.name)
    print('------')


# Test bot
bot.run('Discord_Bot_Key')
