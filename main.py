from discord.ext import commands
import discord
import logging
import nwbot.config as config


logging.basicConfig(level=config.LOG_LEVEL)
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

cogs = [
    "cogs.owner",
    "cogs.admin",
    "cogs.common",
    "cogs.members",
    "cogs.professions",
]

@bot.event
async def on_ready():
    logging.info("Used Token")
    logging.info('------')
    logging.info(config.DISCORD_TOKEN)
    logging.info('------')
    logging.info("Logged in as")
    logging.info('------')
    logging.info(bot.user.name) # type: ignore
    logging.info(bot.user.id)   # type: ignore
    logging.info('------')
    await bot.change_presence(activity=discord.Game(name='New World', type=1))


def main():
    for cog in cogs:
        bot.load_extension(cog)
    bot.run(config.DISCORD_TOKEN, reconnect=True)

if __name__ == "__main__":
    main()
