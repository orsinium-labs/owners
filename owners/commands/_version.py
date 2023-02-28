from __future__ import annotations

from argparse import ArgumentParser

from ._base import Command


class Version(Command):
    """Print the version of the tool.
    """

    @staticmethod
    def init_parser(parser: ArgumentParser) -> None:
        pass

    def run(self) -> int:
        from owners import __version__
        self.print(__version__)
        return 0
