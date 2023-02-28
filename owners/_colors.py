from __future__ import annotations

from dataclasses import dataclass
from typing import Any


RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[94m'
MAGENTA = '\033[35m'
END = '\033[0m'


@dataclass
class Colors:
    disabled: bool

    def green(self, text: Any) -> str:
        if self.disabled:
            return str(text)
        return f'{GREEN}{text}{END}'

    def red(self, text: Any) -> str:
        if self.disabled:
            return str(text)
        return f'{RED}{text}{END}'

    def blue(self, text: Any) -> str:
        if self.disabled:
            return str(text)
        return f'{BLUE}{text}{END}'

    def magenta(self, text: Any) -> str:
        if self.disabled:
            return str(text)
        return f'{MAGENTA}{text}{END}'

    def yellow(self, text: Any) -> str:
        if self.disabled:
            return str(text)
        return f'{YELLOW}{text}{END}'
