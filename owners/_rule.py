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
            paths = [path.absolute() for path in self.root.glob(raw)]
            paths_set = set(paths)
            # remove paths that are children of other paths
            deduplicated = []
            for path in paths:
                if not set(path.parents) & paths_set:
                    deduplicated.append(path)
            return tuple(deduplicated)

        path = Path(raw)
        if not path.exists():
            return tuple()
        return (path.absolute(),)

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
