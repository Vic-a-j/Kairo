from __future__ import annotations

from dataclasses import dataclass

import jmespath

@dataclass
class Filter:
    path: str
    to_value: str

class Mutation():

    def __init__(self, filter: Filter = None):
        self.filter = filter
    

    def mutate(self, request: dict) -> dict:
        if self.filter:
            request = self._apply_filter(request)

        return request
    

    def _apply_filter(self, request: dict) -> dict:
        match = jmespath.search(self.filter.to_value, request)

        if not match:
            return request
        
        curr = request
        filter_path = self.filter.path.split(".")

        for path in filter_path[:-1]:
            if path not in curr:
                raise ValueError("Cannot apply filter given the path.")
            curr = curr.get(path)

        curr[filter_path[-1]] = match
        return request
