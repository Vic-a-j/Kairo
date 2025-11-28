from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jmespath


@dataclass
class Filter:
    path: str
    to_value: str

class Mutation:

    def __init__(self, filter: Filter):
        self.filter = filter
    

    def mutate(self, request: dict[str, Any]) -> dict[str, Any]:
        """Mutate payload request by applying the filter if present."""
        if self.filter:
            request = self._apply_filter(request)

        return request
    

    def _apply_filter(self, request: dict[str, Any]) -> dict[str, Any]:
        """Apply filtering logic from jmespath within given request."""
        match = jmespath.search(self.filter.to_value, request)

        if not match:
            return request
        
        curr_dict: Any = request
        filter_path = self.filter.path.split(".")

        for path_str in filter_path[:-1]:
            if path_str not in curr_dict or not isinstance(curr_dict.get(path_str), dict):
                raise ValueError("Cannot apply filter given the path.")
            curr_dict = curr_dict.get(path_str)

        curr_dict[filter_path[-1]] = match
        return request
