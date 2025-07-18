# calmoji/ebi48.py

import datetime
from typing import Mapping

"""
EBI48_CLOCK — The Canonical Emoji Time Table

Maps 48 half-hour slots to unique, symbolic glyphs (animals, terrain, mythic nature). 
Each UTC day is split into 30min blocks beginning at 00:05. 

Slots:
  slot 0 = 00:05–00:30 → 🐶 Dog Face
  slot 1 = 00:35–01:00 → 🦨 Skunk Face
  ...
  slot 47 = 23:35–00:00 → 🦈 Shark Face

Designed for symbolic scheduling, neurodiverse rhythm anchoring, and low-bandwidth human-AI coordination.
"""

EBI48_CLOCK: Mapping[int, tuple[str, str]] = {
    0:  ("🐶", "Dog Face"),
    1:  ("🦨", "Skunk Face"),
    2:  ("🐱", "Cat Face"),
    3:  ("🐦", "Bird Face"),
    4:  ("🐭", "Mouse Face"),
    5:  ("🦢", "Swan Face"),
    6:  ("🦝", "Raccoon Face"),
    7:  ("🦚", "Peacock Face"),
    8:  ("🐰", "Bunny Face"),
    9:  ("🦦", "Otter Face"),
    10: ("🦊", "Fox Face"),
    11: ("🦫", "Beaver Face"),
    12: ("🐻", "Bear Face"),
    13: ("🦙", "Llama Face"),
    14: ("🐴", "Horse Face"),
    15: ("🦌", "Deer Face"),
    16: ("🐐", "Goat Face"),
    17: ("🦥", "Sloth Face"),
    18: ("🐯", "Tiger Face"),
    19: ("🐘", "Elephant Face"),
    20: ("🦁", "Lion Face"),
    21: ("🐷", "Pig Face"),
    22: ("🦬", "Bison Face"),
    23: ("🐗", "Boar Face"),
    24: ("🐸", "Frog Face"),
    25: ("🦎", "Lizard Face"),
    26: ("🪱", "Worm Face"),
    27: ("🕊️", "Dove Face"),
    28: ("🐔", "Chicken Face"),
    29: ("🌲", "Tree Face"),
    30: ("🦔", "Hedgehog Face"),
    31: ("🪿", "Goose Face"),
    32: ("🦡", "Badger Face"),
    33: ("🦃", "Turkey Face"),
    34: ("🦜", "Parrot Face"),
    35: ("🦉", "Owl Face"),
    36: ("🐺", "Wolf Face"),
    37: ("🦇", "Bat Face"),
    38: ("🦆", "Duck Face"),
    39: ("🪺", "Nest Face"),
    40: ("⛰️", "Mountain Face"),
    41: ("🐢", "Turtle Face"),
    42: ("🦭", "Seal Face"),
    43: ("🐵", "Monkey Face"),
    44: ("🦑", "Squid Face"),
    45: ("🐙", "Octopus Face"),
    46: ("🐠", "Fish Face"),
    47: ("🦈", "Shark Face")
}

def get_emoji_for_time(dt: datetime.datetime) -> tuple[str, str]:
    """
    Map a datetime to a clock index in the 48-slot emoji face table.
    Each hour has two slots:
      - hh:05 → even slot
      - hh:35 → odd slot
    """
    hour = dt.hour
    minute = dt.minute

    if 0 <= minute < 15:
        slot = hour * 2
    elif 30 <= minute < 45:
        slot = hour * 2 + 1
    else:
        raise ValueError(f"Invalid start time for emoji mapping: {dt.isoformat()}")

    return get_emoji_for_slot(slot)

def get_slot_index_for_emoji(emoji: str) -> int:
    for idx, (e, _) in EBI48_CLOCK.items():
        if e == emoji:
            return idx
    raise ValueError(f"Emoji {emoji} not found in clock.")

def get_emoji_for_slot(slot: int) -> tuple[str, str]:
    """Return (emoji, face name) for a given 0–47 slot index."""
    return EBI48_CLOCK.get(slot, ("❓", "Unknown Face"))

def get_emoji_name_for_slot(slot: int) -> str:
    """Return only the face name for a given slot index."""
    return EBI48_CLOCK.get(slot, ("❓", "Unknown Face"))[1]

def get_all_ebi48_slots() -> list[tuple[int, str, str]]:
    return [(i, emoji, label) for i, (emoji, label) in EBI48_CLOCK.items()]
