from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from ._base import Command


class Tree(Command):
    """Show file tree with ownership info.
    """

    @staticmethod
    def init_parser(parser: ArgumentParser) -> None:
        Command.init_parser(parser)

    def run(self) -> int:
        self._inspect(self.code_owners.root)
        return 0

    def _inspect(self, root: Path) -> None:
        for path in sorted(root.iterdir()):
            if not path.is_dir():
                continue
            rule = self.code_owners.find_rule(path)
            if rule is not None:
                self.print(self.colors.green(path.name))
                continue

            self.print(self.colors.red(path.name))
