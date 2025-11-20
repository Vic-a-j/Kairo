from __future__ import annotations

from canary import Canary
from mutation import Mutation

from .utils import get_data

class Kairo():

    def __init__(self, canaries: list[Canary] = None):
        self.canaries = canaries or []

    def load_from_yaml(self, yaml_path: str) -> None:
        data = get_data(yaml_path)
        ...

    def load_from_json(self, json: str) -> None:
        ...

    def load_to_yaml(self, yaml_path: str):
        ...

    def load_to_json(self) -> dict:
        ...

    def run(self, request: dict) -> dict:
        ...

    def add_canary(self, canary: Canary):
        self.canaries.append(canary)


if __name__ == "__main__":
    kairo_instance = Kairo()