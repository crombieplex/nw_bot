from discord.ext import commands
import discord
import nwbot.config as config


class MembersCog(commands.Cog, name="Members"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        message = (f'Hi {member.display_name}!\n'
                    'Wenn Du Mitglied der New World Gilde One Hit Wonder GmbH bist, '
                    'setze doch bitte deinen InGame Namen als nickname.\n'
                    'Damit ist gewährleistet, dass Dich die anderen auch wiedererkennen.\n'
                    'Und Jetzt wünsche ich Dir viel Spaß auf unserem Discord!')
        await member.send(message)

def setup(bot):
    bot.add_cog(MembersCog(bot))