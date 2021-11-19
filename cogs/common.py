from discord.ext import commands
from discord.ext.commands.core import command
import logging


class Common(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(hidden=True)
    async def hello(self, ctx: commands.Context) -> None:
        '''Test Function that greets you'''
        logging.info("got hello command")
        await ctx.send(f"Hey {ctx.author}")


def setup(bot):
    bot.add_cog(Common(bot))