from __future__ import annotations

from types import MappingProxyType

from ._base import Command
from ._owners_of import OwnersOf
from ._owned_by import OwnedBy
from ._version import Version


commands: MappingProxyType[str, type[Command]]
commands = MappingProxyType({
    'owned-by': OwnedBy,
    'owners-of': OwnersOf,
    'version': Version,
})

__all__ = [
    'commands',
    'Command',
]
