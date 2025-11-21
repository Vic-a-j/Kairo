from __future__ import annotations

from dataclasses import dataclass

@dataclass
class Filter:
    path: str
    to_value: str

class Mutation():

    def __init__(self, filter: Filter = None):
        self.filter = filter
    
    
    def mutate(self, request: dict) -> dict:
        return request