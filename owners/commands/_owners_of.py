from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from ._base import Command


class OwnersOf(Command):
    """Show owners of the given file.
    """

    @staticmethod
    def init_parser(parser: ArgumentParser) -> None:
        Command.init_parser(parser)
        parser.add_argument('paths', nargs='+')

    def run(self) -> int:
        paths = [Path(p).absolute() for p in self.args.paths]
        found = False
        for rule in self.code_owners.rules:
            if not any(rule.includes(p) for p in paths):
                continue
            for owner in rule.owners:
                self.print(owner)
                found = True
        return int(not found)
