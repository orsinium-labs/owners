from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ._rule import Rule


@dataclass(frozen=True)
class Section:
    root: Path
    raw: str
    rules: tuple[Rule, ...]

    @cached_property
    def name(self) -> str | None:
        raw = self.raw.strip()
        without_comments = raw.split('#')[0]
        if not raw:
            return None
        return without_comments.lstrip('^[').rstrip(']')

    @cached_property
    def required(self) -> bool:
        return not self.raw.lstrip().startswith('^')

    def find_rule(self, path: Path) -> Rule | None:
        path = path.absolute()
        for rule in reversed(self.rules):
            if path in rule.paths:
                return rule
        for rule in reversed(self.rules):
            if rule.includes(path):
                return rule
        return None
