from discord.ext import commands
import discord
import nwbot.config as config


class MembersCog(commands.Cog, name="Members"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        message = (f'Hi {member.display_name}!\n'
                    'Please set your ingame name as your Discord nickname, '
                    'this will help others to recognize you.')
        await member.send(message)

def setup(bot):
    bot.add_cog(MembersCog(bot))
