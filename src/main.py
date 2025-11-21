from __future__ import annotations

from canary import Canary
from condition import Condition, Match
from mutation import Mutation, Filter

from .utils import get_yaml_data, get_json_data

class Kairo():

    def __init__(self, canaries: list[Canary] = None):
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


    def create_canaries(self, canaries: list[dict]) -> None:
        for canary in canaries:
            name = canary["name"]
            canary_condition = canary.get("condition")
            canary_mutations = canary.get("mutations")
            canary_config = canary.get("config", {})

            self.canaries.append(
                Canary(
                    name,
                    condition = self._create_condition(canary_condition),
                    mutations = self._create_mutations(canary_mutations),
                    config = canary_config,
                )
            )

    
    def _create_condition(self, condition_dict: dict) -> Condition:
        match_dict = condition_dict.get("match", {})
        match = Match(
                path=match_dict.get("path"),
                with_value=match_dict.get("to_value"),
            )
        return Condition(match)


    def _create_mutations(self, mutations_list: list[dict]) -> list[Mutation]:
        mutations = []
        for mutation in mutations_list:
            if "filter" in mutation:
                filter = Filter(
                    path=mutation["filter"]["path"],
                    to_value=mutation["filter"]["to_value"]
                )
                mutation = Mutation(filter)
                mutations.append(mutation)
        return mutations
        

    def run(self, request: dict) -> dict:
        """Run conditions and mutations from given request."""

        for canary in self.canaries:
            try:
                request = canary.evaluate(request)
            except Exception as e:
                print(f"Error while processing Canary '{canary.name}': {e}")

        return request


if __name__ == "__main__":
    kairo_instance = Kairo()