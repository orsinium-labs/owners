from __future__ import annotations

from types import MappingProxyType

from ._base import Command
from ._version import Version


commands: MappingProxyType[str, type[Command]]
commands = MappingProxyType({
    'version': Version,
})

__all__ = [
    'commands',
    'Command',
]
