import discord
from dataclasses import dataclass


@dataclass
class Crafter:
    """ Class that represents a member with a specific Profession """
    id: int
    name: str
    profession_lvl: int

    @classmethod
    def from_discord_member(cls, discord_member: discord.Member):
        return cls(discord_member.id, discord_member.display_name, profession_lvl = 0)
