from __future__ import annotations

from mutation import Mutation
from condition import Condition

class Canary():

    def __init__(self, name: str, *, condition: Condition = None, mutations: list[Mutation] = None, config: dict = None):
        self.name = name
        self.condition = condition
        self.mutations = mutations
        self.config = config

    def add_condition(self, condition: Condition) -> None:
        if self.condition is not None:
            raise ValueError("Cannot add alredy existing condition to Canary.")
            
        self.condition = condition
    
    def add_mutation(self, mutation: Mutation) -> None:
        self.mutations.append(mutation)
        return

    def add_config(self, new_config: dict) -> None:
        self.config = new_config
        return
    
    def _deep_merge(self, config_dict: dict, request_dict: dict) -> dict:
        """Recursively mere config dict into request dict."""
        for key, value in config_dict.items():
            if key in request_dict and isinstance(request_dict[key], dict) and isinstance(value, dict):
                self._deep_merge(value, request_dict[key])
            else:
                request_dict[key] = value

        return request_dict

    def evaluate(self, request: dict, override: bool) -> dict:
        """Evaluate request to a mutation"""
        if not self.condition and not self.mutations:
            raise ValueError("Cannot evaluate Canary without condition or mutation.")
        
        if self.condition and not self.condition.matches(request):
            raise ValueError("Condition provided, but did not match inside request.")
        
        if self.mutations:
            for mutation in self.mutations:
                request = mutation.mutate(request)

        if self.config and override:
            request.update(self.config)
        
        if self.config and not override:
            request = self._deep_merge(self.config, request)

        return request