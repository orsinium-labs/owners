from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Iterator

from ._rule import Rule
from ._section import Section


@dataclass(frozen=True)
class CodeOwners:
    root: Path

    @cached_property
    def file_path(self) -> Path:
        paths = [
            self.root / 'CODEOWNERS',
            self.root / 'docs' / 'CODEOWNERS',
            self.root / '.gitlab' / 'CODEOWNERS',
        ]
        for path in paths:
            if path.exists():
                return path
        raise FileNotFoundError('cannot find CODEOWNERS')

    @cached_property
    def sections(self) -> tuple[Section, ...]:
        sections: list[Section] = []
        section_name = ''
        rules: list[Rule] = []
        with self.file_path.open('r', encoding='utf8') as stream:
            for line in stream:
                line = line.strip()

                # comment line
                if not line or line.startswith('#'):
                    continue
                is_section = line.startswith(('^[', '['))

                # rule line
                if not is_section:
                    rules.append(Rule(root=self.root, raw=line))
                    continue

                # section line
                if rules:
                    sections.append(Section(
                        root=self.root,
                        raw=section_name,
                        rules=tuple(rules),
                    ))
                section_name = line
                rules = []

        if rules:
            sections.append(Section(
                root=self.root,
                raw=section_name,
                rules=tuple(rules),
            ))
        return tuple(sections)

    @property
    def rules(self) -> Iterator[Rule]:
        for section in self.sections:
            yield from section.rules

    def find_rule(self, path: Path) -> Rule | None:
        for section in reversed(self.sections):
            rule = section.find_rule(path)
            if rule is not None:
                return rule
        return None
