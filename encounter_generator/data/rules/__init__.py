"""
D&D 5e Rules Data Package

This package contains structured data for D&D 5e game rules including:
- Character classes
- Species/races
- Backgrounds
- Feats
- Spell progression tables
- Game rules and constants
"""

from .spell_tables import (
    FULL_CASTER_SLOTS,
    HALF_CASTER_SLOTS,
    THIRD_CASTER_SLOTS,
    PACT_MAGIC_SLOTS
)

from .classes import BARBARIAN, BARD

__all__ = [
    'FULL_CASTER_SLOTS',
    'HALF_CASTER_SLOTS',
    'THIRD_CASTER_SLOTS',
    'PACT_MAGIC_SLOTS',
    'BARBARIAN',
    'BARD',
]
