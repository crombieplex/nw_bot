from dataclasses import dataclass, field
from nwbot.crafter import Crafter
from typing import List, Dict
import discord


@dataclass
class Profession:
    """ Class that represents a New World Profession """
    name: str
    _all_crafters: Dict[int, Crafter] = field(default_factory=dict)

    def get_top_n_crafters(self, n) -> List[Crafter]:
        sorted_crafters = sorted(self._all_crafters.values(), key=lambda x: x.profession_lvl, reverse=True)
        if n > len(sorted_crafters):
            return sorted_crafters
        return sorted_crafters[:n]
    
    def add_crafter(self, crafter: discord.Member, profession_level: int) -> None:
        if crafter.id in self._all_crafters:
            raise KeyError("User already exists")
        new_crafter = Crafter.from_discord_member(crafter)
        new_crafter.profession_lvl = profession_level
        self._all_crafters[crafter.id] = new_crafter
    
    def remove_crafter(self, crafter: discord.Member) -> None:
        self._all_crafters.pop(crafter.id, None)

    def get_crafter(self, crafter: discord.Member) -> Crafter:
        if crafter.id not in self._all_crafters:
            raise KeyError("User does not exist")
        return self._all_crafters[crafter.id]

    def update_crafter_level(self, crafter: discord.Member, profession_level: int) -> None:
        if crafter.id not in self._all_crafters:
            raise KeyError("User does not exist")
        if crafter.display_name != self._all_crafters[crafter.id].name:
            self._all_crafters[crafter.id].name = crafter.display_name
        self._all_crafters[crafter.id].profession_lvl = profession_level

