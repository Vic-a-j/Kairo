from __future__ import annotations

from mutation import Mutation

class Canary():

    def __init__(self, name: str, condition: str = None, config: dict = None, mutations: list[Mutation] = None):
        self.name = name
        self.condition = condition
        self.mutations = mutations
        self.config = config

    def add_condition(self, condition: str) -> None:
        if self.condition is not None:
            raise ValueError("Cannot add alredy existing condition to Canry.")
            
        self.condition = condition
    
    def add_mutation(self, mutation: Mutation) -> None:
        ...

    def add_config(self, new_config: dict) -> None:
        self.config = new_config
        return

    def evaluate(self) -> None:
        ...