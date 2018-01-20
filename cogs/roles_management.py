import discord
import utils.data as data
from utils.roles import get_role, get_next_role, get_previous_role, roles, roles_list
from discord.ext import commands
import discord.errors
import asyncio


class Roles:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def set(self, ctx, user: discord.Member, role: discord.Role):
        await self.bot.add_roles(user, role)
        await self.bot.change_nickname(user, user.name + ' [{}]'.format(role.name))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def invites(self, ctx):
        """Shows the invites, only in invite-counter"""
        author = ctx.message.author
        has_rank = False
        msg = None
        msg2 = None
        for user_invite in data.users_invites.values():
            if user_invite[0].id == author.id:
                role = discord.utils.get(data.server.roles, name=get_role(user_invite[1]))
                if role is None:
                    await self.bot.say('{}\nYou have {} invites!\nYou need 25 invite to become VIP!'
                                       .format(ctx.message.author.mention, user_invite[1]))
                    has_rank = True
                    continue
                if role not in author.roles:
                    if author.top_role.name in roles_list:
                        await self.bot.remove_roles(author, author.top_role)
                    await self.bot.add_roles(author, role)
                    await self.bot.change_nickname(author, author.name + '[{}]'.format(role.name))
                    await self.bot.send_message(author, '{} Congratulations, you are now {}'.format(author.mention,
                                                                                                     get_role(user_invite[1])))
                next_rank, invites_needed = get_next_role(user_invite[1])
                msg = await self.bot.say('<@{}>\nYou have {} invites\n{} more to become {}'
                                         .format(user_invite[0].id, user_invite[1], invites_needed - user_invite[1],
                                                 next_rank))
                has_rank = True
        if not has_rank:
            msg = await self.bot.say('<@{}>\nYou have no invites!\nYou need 25 invites to be VIP!'
                                     .format(ctx.message.author.id))

    @commands.command(pass_context=True)
    async def rank(self, ctx):
        """Shows the roles affiliate level"""
        message = ''
        for invites, rank in roles.items():
            message += '**{}** - {} invites\n'.format(rank, invites)
        embed = discord.Embed(title='Affiliate Rank', description=message, color=0xfff71e)
        msg = await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def members(self, ctx):
        """Shows somse info"""
        everyone = data.server.members
        members = list(filter(lambda x: not x.bot, everyone))
        online_members = list(filter(lambda x: not x.status.value == 'offline', members))
        embed = discord.Embed(title='Server members', description='------------------\n''**Online members:** {}'
                                                                  '\n**Total members:** {}'
                              .format(online_members.__len__(), members.__len__()), color=0xfff71e)
        msg = await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def random_member(self, ctx):
        """Use this once, before everrything"""
        msg = await self.bot.say('There is no contest being held at the moment...\n')


async def rli(bot):
    # Get the current invites
    await asyncio.sleep(5)
    while not bot.is_closed:
        # Check if server is ready and registered
        if data.server is None:
            continue
        current_invites = await bot.invites_from(data.server)
        for invite in current_invites:
            # User inviter
            inviter = invite.inviter
            if inviter.id not in data.users_invites:
                data.users_invites[inviter.id] = [inviter, 0]
            if invite.id not in data.invites:
                data.invites[invite.id] = invite
                data.users_invites[inviter.id][1] += invite.uses
            else:
                old_uses = data.invites[invite.id].uses
                difference = invite.uses - old_uses
                data.invites[invite.id] = invite
                data.users_invites[inviter.id][1] += difference
        await asyncio.sleep(35)


def setup(bot: commands.Bot):
    bot.add_cog(Roles(bot))
    bot.loop.create_task(rli(bot))
