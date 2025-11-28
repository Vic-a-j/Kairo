import pytest

from kairo.canary import Canary
from kairo.condition import Condition, Match
from kairo.mutation import Filter, Mutation


def test_add_condition_success():
    canary = Canary("test")
    condition = Condition(Match(path="foo", with_value="bar"))
    canary.add_condition(condition)

    assert canary.condition == condition

def test_add_condition_already_exists():
    canary = Canary("test", condition=Condition(Match(path="foo", with_value="bar")))
    with pytest.raises(ValueError, match="Cannot add alredy existing condition to Canary."):
        canary.add_condition(Condition(Match(path="baz", with_value="qux")))

def test_add_mutation_to_none():
    canary = Canary("test")
    mutation = Mutation(Filter(path="foo", to_value="bar"))
    canary.add_mutation(mutation)

    assert canary.mutations == [mutation]

def test_add_mutation_to_existing_list():
    mutation1 = Mutation(Filter(path="foo", to_value="bar"))
    mutation2 = Mutation(Filter(path="baz", to_value="qux"))
    canary = Canary("test", mutations=[mutation1])
    canary.add_mutation(mutation2)

    assert canary.mutations == [mutation1, mutation2]

def test_add_config():
    canary = Canary("test")
    config = {"key": "value"}
    canary.add_config(config)
    
    assert canary.config == config