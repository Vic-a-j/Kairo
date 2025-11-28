from __future__ import annotations

from typing import Any

from .canary import Canary
from .condition import Condition, Match
from .mutation import Filter, Mutation
from .utils import get_json_data, get_yaml_data


class Kairo:

    def __init__(self, canaries: list[Canary] | None = None):
        self.canaries = canaries or []


    def load_from_yaml(self, yaml_path: str) -> None:
        """Load canaries from yaml path."""
        data = get_yaml_data(yaml_path)
        canaries = data.get("global_config", {}).get("canaries", [])

        self.create_canaries(canaries)


    def load_from_json(self, json_str: str) -> None:
        """Load canaries from json path."""
        data = get_json_data(json_str)
        canaries = data.get("global_config", {}).get("canaries", [])

        self.create_canaries(canaries)


    def add_canary(self, canary: Canary) -> None:
        """Add a canary to process."""
        self.canaries.append(canary)


    def create_canaries(self, canaries: list[dict[str, Any]]) -> None:
        """Create canaries from configuration."""
        for canary in canaries:
            name = canary["name"]
            canary_condition = canary.get("condition")
            canary_mutations = canary.get("mutations")
            canary_config = canary.get("config", {})

            self.canaries.append(
                Canary(
                    name,
                    condition = self._create_condition(canary_condition) if canary_condition else None,
                    mutations = self._create_mutations(canary_mutations) if canary_mutations else None,
                    config = canary_config if canary_config else None,
                )
            )

    
    def _create_condition(self, condition_dict: dict[str, Any]) -> Condition:
        """Create condition object."""
        match_dict = condition_dict.get("match", {})
        match_obj = Match(
                path=match_dict.get("path"),
                with_value=match_dict.get("with_value"),
            )
        return Condition(match_obj)


    def _create_mutations(self, mutations_list: list[dict[str, Any]]) -> list[Mutation]:
        """Create list of mutation objects."""
        mutations = []
        for mutation in mutations_list:
            if "filter" in mutation:
                filter_obj = Filter(
                    path=mutation["filter"]["path"],
                    to_value=mutation["filter"]["to_value"]
                )
                mutations.append(Mutation(filter_obj))
        return mutations
        

    def run(self, request: dict[str, Any], override: bool = True) -> dict[str, Any]:
        """Run conditions and mutations from given request."""
        for canary in self.canaries:
            try:
                request = canary.evaluate(request, override)
            except Exception as e:
                print(f"Error while processing Canary '{canary.name}': {e}")

        return request


if __name__ == "__main__":
    ### Example usage:
    # kairo = Kairo()
    # kairo.load_from_yaml("canaries.yaml")
    # result = kairo.run({"some": "request"})
    pass