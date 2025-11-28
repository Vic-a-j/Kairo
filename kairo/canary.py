from __future__ import annotations

from typing import Any

from .condition import Condition
from .mutation import Mutation


class Canary:

    def __init__(self, name: str, *, condition: Condition | None = None, mutations: list[Mutation] | None = None, config: dict[str, Any] | None = None):
        self.name = name
        self.condition = condition
        self.mutations = mutations
        self.config = config

    def add_condition(self, condition: Condition) -> None:
        """Add a condition to the Canary."""
        if self.condition is not None:
            raise ValueError("Cannot add alredy existing condition to Canary.")
            
        self.condition = condition
    
    def add_mutation(self, mutation: Mutation) -> None:
        """Add a mutation to the Canary."""
        if self.mutations:
            self.mutations.append(mutation)
            return
          
        self.mutations = [mutation]

    def add_config(self, new_config: dict[str, Any]) -> None:
        """Add config to the Canary."""
        self.config = new_config
        return
    
    def _deep_merge(self, config_dict: dict[str, Any], request_dict: dict[str, Any]) -> dict[str, Any]:
        """Recursively mere config dict into request dict."""
        for key, value in config_dict.items():
            if key in request_dict and isinstance(request_dict[key], dict) and isinstance(value, dict):
                self._deep_merge(value, request_dict[key])
            else:
                request_dict[key] = value

        return request_dict

    def evaluate(self, request: dict[str, Any], override: bool = True) -> dict[str, Any]:
        """
        Evaluate request with condition and mutations.

        Args:
            request (Dict): The request payload.
            override (bool): If True, config replaces request; else, config is merged.

        Returns:
            request (Dict): The evaluated request.

        Raises:
            ValueError: If condition or mutation requirements are not met.
        """

        # Neither condition or mutation are met
        if not self.condition and not self.mutations:
            raise ValueError("Cannot evaluate Canary without condition or mutation.")
        
        # Condition does not match request
        if self.condition and not self.condition.matches(request):
            raise ValueError("Condition provided, but did not match inside request.")
        
        # Add mutations
        if self.mutations:
            for mutation in self.mutations:
                request = mutation.mutate(request)

        # If override, it replaces original config
        if self.config and override:
            request.update(self.config)
        
        # If not override, it keeps original config through deep merge
        if self.config and not override:
            request = self._deep_merge(self.config, request)

        return request