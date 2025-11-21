from __future__ import annotations

from mutation import Mutation
from condition import Condition

class Canary():

    def __init__(self, name: str, *, condition: Condition = None, mutations: list[Mutation] = None, config: dict = None):
        self.name = name
        self.condition = condition
        self.mutations = mutations
        self.config = config

    def add_condition(self, condition: str) -> None:
        if self.condition is not None:
            raise ValueError("Cannot add alredy existing condition to Canary.")
            
        self.condition = condition
    
    def add_mutation(self, mutation: Mutation) -> None:
        self.mutations.append(mutation)
        return

    def add_config(self, new_config: dict) -> None:
        self.config = new_config
        return

    def evaluate(self, request: dict) -> dict:
        """Evaluate request to a mutation"""
        if not self.condition and not self.mutations:
            raise ValueError("Cannot evaluate Canary without condition or mutation.")
        
        if self.condition and not self.condition.matches(request):
            raise ValueError("Condition provided, but did not match inside request.")
        
        if self.mutations:
            for mutation in self.mutations:
                request = mutation.mutate(request)

        if self.config:
            request.update(self.config)

        return request