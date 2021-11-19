from discord.ext import commands
from discord.commands import slash_command, permissions
from discord import DMChannel
import nwbot.config as config
import asyncio

class AdminCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # Guild Slash Command Example with Role Permissions
    @slash_command(name="clear", guild_ids=[config.guild_id], default_permission=False, description="Clear all messages except the pinned ones from this channel")
    @permissions.has_role("admin")
    async def clear_channel(self, ctx):
        channel = ctx.channel
        if channel is not None and not isinstance(channel, DMChannel):
            await channel.purge(check=lambda m: not m.pinned)
            msg = await ctx.respond("Channel cleared")
            response = await msg.original_message()
            await asyncio.sleep(5)
            await response.delete()

def setup(bot):
    bot.add_cog(AdminCog(bot))
