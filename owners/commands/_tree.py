from __future__ import annotations

from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Callable

from ._base import Command


class Cov(Enum):
    FULL = 'full'  # the dir is 100% owned
    MOST = 'most'  # not the dir itself but everything inside is owned
    PART = 'part'  # some subdirs in the dir are owned
    NONE = 'none'  # nothing in the dir is owned


# Directories to skip by default
IGNORE = frozenset({'.git', '__pycache__'})


@dataclass
class PathInfo:
    # path to the analyzed dir
    path: Path

    # information about all subdirs, None if not analyzed (because the root is owned)
    children: list[PathInfo] | None

    # the owner team, empty string for not directly owned dirs
    owner: str

    @cached_property
    def cov(self) -> Cov:
        if self.children is None:
            return Cov.FULL
        if not self.children:
            return Cov.NONE
        if all(p.cov in (Cov.FULL, Cov.MOST) for p in self.children):
            return Cov.MOST
        if all(p.cov == Cov.NONE for p in self.children):
            return Cov.NONE
        return Cov.PART


class Tree(Command):
    """Show file tree with ownership info.
    """

    @staticmethod
    def init_parser(parser: ArgumentParser) -> None:
        Command.init_parser(parser)

    def run(self) -> int:
        path_info = self._inspect(self.code_owners.root)
        self._show_tree(path_info, 0)
        return 0

    def _inspect(self, root: Path) -> PathInfo:
        rule = self.code_owners.find_rule(root)
        if rule is not None:
            return PathInfo(root, children=None, owner=rule.owners[0])

        path_infos: list[PathInfo] = []
        for path in sorted(root.iterdir()):
            if not path.is_dir():
                continue
            if path.name in IGNORE:
                continue
            path_infos.append(self._inspect(path))
        return PathInfo(root, children=path_infos, owner='')

    def _show_tree(self, info: PathInfo, level: int) -> None:
        if info.cov == Cov.FULL:
            self._show_path(self.colors.green, info, level)
            return
        if info.cov == Cov.MOST:
            self._show_path(self.colors.blue, info, level)
            return
        if info.cov == Cov.NONE:
            self._show_path(self.colors.red, info, level)
            return
        if info.cov == Cov.PART:
            assert info.children
            self._show_path(self.colors.yellow, info, level)
            for child in info.children:
                self._show_tree(child, level + 1)
            return
        raise RuntimeError('unreachable')

    def _show_path(self, color: Callable, info: PathInfo, level: int) -> None:
        width = level * 2 + len(info.path.name) + 1
        ident = 60 - width
        self.print(' |' * level, color(info.path.name), ' ' * ident + info.owner)
