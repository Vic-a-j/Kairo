from __future__ import annotations

from dataclasses import dataclass
from typing import Any

@dataclass
class Match:
    path: str
    with_value: Any

class Condition():

    def __init__(self, match: Match):
        self.match = match

    def matches(self, request) -> bool:
        return self.match.with_value == self._find_value(request)
    
    def _find_value(self, request) -> Any:
        curr = request
        for path in self.match.path.split("."):
            if path not in curr:
                return None
            
            curr = curr.get(path)
        return curr

