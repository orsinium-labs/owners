from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path


@dataclass(frozen=True)
class Rule:
    root: Path
    raw: str

    @cached_property
    def raw_path(self) -> str:
        return self.raw.split()[0]

    @cached_property
    def paths(self) -> tuple[Path, ...]:
        raw = self.raw_path.lstrip('/')
        if '*' in raw:
            paths = self.root.glob(raw)
            return tuple(path.absolute() for path in paths)
        path = Path(raw)
        if not path.exists():
            return tuple()
        return (path,)

    @cached_property
    def owners(self) -> tuple[str, ...]:
        without_comments = self.raw.split('#')[0]
        return tuple(without_comments.split()[1:])

    def includes(self, path: Path) -> bool:
        """Check if the given path is included in the rule.
        """
        path = path.absolute()
        if path in self.paths:
            return True
        for parent in path.parents:
            if parent in self.paths:
                return True
        return False
