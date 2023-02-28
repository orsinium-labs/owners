from __future__ import annotations

from argparse import ArgumentParser

from ._base import Command


class OwnedBy(Command):
    """Show paths owned by the given user or group.
    """

    @staticmethod
    def init_parser(parser: ArgumentParser) -> None:
        Command.init_parser(parser)
        parser.add_argument('owners', nargs='+')

    def run(self) -> int:
        owners = set(self.args.owners)
        root = self.code_owners.root
        for rule in self.code_owners.rules:
            if not owners & set(rule.owners):
                continue
            for path in rule.paths:
                path = path.relative_to(root)
                self.print(str(path))
        return 0
