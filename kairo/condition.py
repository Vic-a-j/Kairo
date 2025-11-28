from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Match:
    path: str
    with_value: Any

class Condition:

    def __init__(self, match: Match):
        self.match = match

    def matches(self, request: dict[str, Any]) -> bool:
        """Returns matching condition from yaml path."""
        return bool(self.match.with_value == self._find_value(request))
    
    def _find_value(self, request: dict[str, Any]) -> Any:
        """Finds value given path."""
        curr_dict: Any = request
        for path_str in self.match.path.split("."):
            if path_str not in curr_dict:
                return None
            
            curr_dict = curr_dict.get(path_str)
        return curr_dict

