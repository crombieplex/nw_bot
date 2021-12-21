from discord import Embed
from discord.commands import Option, permissions, user_command, message_command, slash_command
from discord.ext import commands
from nwbot.crafter import Crafter
from nwbot.profession import Profession
from tabulate import tabulate
from typing import Dict
import asyncio
import discord
import nwbot.config as config
import os
import pickle


class ProfessionsCog(commands.Cog, name="Professions"):
    def __init__(self, bot):
        self.bot = bot
        self.profession_data: Dict[str, Profession] = {}
        self.profession_channel_id = None
        if os.path.exists(config.DB_PATH):
            self._load_data_from_disk()
    

    def _safe_data_to_disk(self):
        data = {}
        data["profession_data"] = self.profession_data
        data["profession_channel_id"] = self.profession_channel_id
        with open(config.DB_PATH, "wb") as f:
            pickle.dump(data, f)

    def _load_data_from_disk(self):
        with open(config.DB_PATH, "rb") as f:
            data = pickle.load(f)
            self.profession_data = data.get("profession_data")
            self.profession_channel_id = data.get("profession_channel_id")

    def _flush_db(self):
        os.remove(config.DB_PATH)
        self.profession_data = {}
    
    def _update_crafter_name(self, crafter_id: int, crafter_name: str) -> None:
        for profession in self.profession_data.values():
            profession.update_crafter_name(crafter_id, crafter_name)

    def _delete_crafter(self, crafter_id: int) -> None:
        for profession in self.profession_data.values():
            profession.remove_crafter(crafter_id)
        
    
    @slash_command(guild_ids=[config.GUILD_ID], description="Setze den Berufs Channel", default_permission=False)
    @permissions.has_role(config.ADMIN_ROLE_NAME)
    async def set_profession_channel(
        self,
        ctx,
        channel: discord.TextChannel
    ):
        self.profession_channel_id = channel.id
        self._safe_data_to_disk()
        await ctx.respond(f"Setze {channel} als Berufe channel", ephemeral=True)
        

    @slash_command(guild_ids=[config.GUILD_ID], description="Setze dein Berufslevel")
    async def set_profession(
        self,
        ctx,
        profession_name: Option(str, "Der Beruf für den das Level gesetzt werden soll", choices=[*config.PROFESSIONS.keys()]), # type: ignore
        level: Option(int, "Das Level des Berufes", default=0) # type: ignore
    ):
        try:
            profession_key = await self.parse_profession(profession_name)
        except KeyError:
            await ctx.respond(f"Beruf {profession_name} nicht gefunden")
            return

        profession = self.profession_data.get(profession_key)
        if not profession:
            profession = Profession(profession_name)
            self.profession_data[profession_key] = profession

        try:
            crafter = profession.get_crafter(ctx.author.id)
        except KeyError:
            crafter = profession.add_crafter(ctx.author.id, ctx.author.display_name, level)

        if crafter.name != ctx.author.display_name:
            self._update_crafter_name(ctx.author.id, ctx.author.display_name) 
        profession.update_crafter_level(crafter.id, level)

        if not self.profession_channel_id:
            await ctx.respond("\n".join([f"{profession_name} level auf {level} gesetzt",
            "Um die Top crafter in einem Channel zu posten muss zuerst ein channel mit /set_profession_channel gesetzt werden"]), ephemeral=True)
            return

        self._safe_data_to_disk()
        asyncio.gather(
            self.update_top_crafters(),
            ctx.respond(f"{profession_name} level auf {level} gesetzt", ephemeral=True)
        )

    async def update_top_crafters(self):
        channel = await self.bot.fetch_channel(self.profession_channel_id)
        await channel.purge()
        for idx, profession in enumerate(self.profession_data.values()):
            table = []
            if idx == 0:
                headers = ["Beruf", "Member", "Skill Level"]
            else:
                headers = []

            top_crafters = profession.get_top_n_crafters(3)
            for crafter in top_crafters:
                row = [profession.name, crafter.name, crafter.profession_lvl]
                table.append(row)
            msg = tabulate(table, headers, tablefmt="github")
            await channel.send(f"```{msg}```")

    async def parse_profession(self, profession: str):
        profession_key = config.PROFESSIONS.get(profession)
        if not profession_key:
            raise KeyError("Profession does not exist")
        return profession_key

    @user_command(name="Show ID", description="Show User ID", guild_ids=[config.GUILD_ID], default_permission=False)
    @permissions.has_role(config.ADMIN_ROLE_NAME)
    async def show_id(self, ctx, user: discord.Member):
        await ctx.respond(user.id, ephemeral=True)

    @message_command(name="Repeat", description="Repeat this message", guild_ids=[config.GUILD_ID])
    async def repeat(self, ctx, message: discord.Message):
        await ctx.respond(message.content, ephemeral=True)

    @slash_command(guild_ids=[config.GUILD_ID], description="Rufe Alle Berufe ab")
    async def get_profession_names(self, ctx):
        await ctx.respond(config.PROFESSIONS, ephemeral=True)

    @slash_command(guild_ids=[config.GUILD_ID], description="Rufe Alle Berufsdaten ab")
    async def get_profession_data(self, ctx):
        await ctx.respond(self.profession_data, ephemeral=True)

    @slash_command(guild_ids=[config.GUILD_ID], description="Rufe die Top5 Mitglieder ab mit genanntem Beruf")
    async def get_profession(self,
        ctx,
        profession_name: Option(str, "Der Beruf für den die Top5 Crafter abgefragt werden sollen", choices=[*config.PROFESSIONS.keys()]), # type: ignore
    ):
        try:
            profession_key = await self.parse_profession(profession_name)
        except KeyError:
            await ctx.respond(f"Beruf {profession_name} nicht gefunden", ephemeral=True)
            return

        if profession_key not in self.profession_data:
            await ctx.respond(f"Keine Daten für den Beruf: {profession_name}", ephemeral=True)
            return
        crafters = self.profession_data[profession_key].get_top_n_crafters(5)

        response = Embed(title="Top 5")
        response.add_field(name="Crafter", value="\n".join([x.name for x in crafters]))
        response.add_field(name="Profession Level", value="\n".join([str(x.profession_lvl) for x in crafters]))
        await ctx.respond(embed=response, ephemeral=True)

    @slash_command(guild_ids=[config.GUILD_ID], description="Lösche Berufsdaten eines Members")
    @permissions.has_role(config.ADMIN_ROLE_NAME)
    async def delete_crafter(self,
        ctx,
        member: discord.Member
    ):
        self._delete_crafter(member.id)
        asyncio.gather(
            ctx.respond(f"Deleted profession data of {member}", ephemeral=True),
            self.update_top_crafters()
        )

    @slash_command(guild_ids=[config.GUILD_ID], description="Lösche Berufsdaten einer ID")
    @permissions.has_role(config.ADMIN_ROLE_NAME)
    async def delete_crafter_by_id(self,
        ctx,
        member_id: str
    ):
        self._delete_crafter(int(member_id))
        asyncio.gather(
            ctx.respond(f"Deleted profession data of {member_id}", ephemeral=True),
            self.update_top_crafters()
        )


def setup(bot):
    bot.add_cog(ProfessionsCog(bot))
