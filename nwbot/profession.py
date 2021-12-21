from dataclasses import dataclass, field
import logging
from nwbot.crafter import Crafter
from typing import List, Dict


@dataclass
class Profession:
    """ Class that represents a New World Profession """
    name: str
    _all_crafters: Dict[int, Crafter] = field(default_factory=dict)

    def get_top_n_crafters(self, n: int) -> List[Crafter]:
        sorted_crafters = sorted(self._all_crafters.values(), key=lambda x: x.profession_lvl, reverse=True)
        if n > len(sorted_crafters):
            return sorted_crafters
        return sorted_crafters[:n]
    
    def add_crafter(self, crafter_id: int, crafter_name: str, profession_level: int) -> Crafter:
        if crafter_id in self._all_crafters:
            raise KeyError("User already exists")
        new_crafter = Crafter(crafter_id, crafter_name, profession_level)
        self._all_crafters[crafter_id] = new_crafter
        return new_crafter
    
    def remove_crafter(self, crafter_id: int) -> None:
        self._all_crafters.pop(crafter_id, None)

    def get_crafter(self, crafter_id: int) -> Crafter:
        if crafter_id not in self._all_crafters:
            raise KeyError("User does not exist")
        return self._all_crafters[crafter_id]

    def update_crafter_level(self, crafter_id: int, profession_level: int) -> None:
        if crafter_id not in self._all_crafters:
            raise KeyError("User does not exist")
        self._all_crafters[crafter_id].profession_lvl = profession_level

    def update_crafter_name(self, crafter_id: int, crafter_name: str) -> None:
        if crafter_id not in self._all_crafters:
            raise KeyError("User does not exist")
        logging.debug(f"Updating crafter name from {self._all_crafters[crafter_id].name} to {crafter_name}")
        self._all_crafters[crafter_id].name = crafter_name

