from __future__ import annotations

from dataclasses import dataclass

@dataclass
class Match:
    path: str
    with_value: str

class Condition():

    def __init__(self, match: Match = None):
        self.match = match

    def matches(self, request) -> bool:
        
        return False