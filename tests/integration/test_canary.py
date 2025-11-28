import pytest

from kairo.canary import Canary
from kairo.condition import Condition, Match
from kairo.mutation import Filter, Mutation


@pytest.mark.parametrize(
    ("match", "filter", "config"), [
        (
            Match(path="request.header", with_value="request.headers[?!(contains(['NO_HEADER_1', 'NO_HEADER_2'], no_val))]"),
            Filter(path="request.fields", to_value=""),
            {"test_config": float("inf")}
        ),
        (
            Match(path="", with_value=""),
            Filter(path="", to_value=""),
            {}
        ),
        (
            Match(path="", with_value=""),
            None,
            None
        ),
        (
            None,
            None,
            None
        ),
    ])
def test_create_canaries(match, filter, config):
    canary_name = "test_name"
    test_condition = Condition(match)
    test_mutation = Mutation(filter)

    test_canary = Canary(canary_name, condition=test_condition, mutations=[test_mutation], config=config)
    assert test_canary.name == canary_name
    assert test_canary.condition == test_condition
    assert test_canary.mutations == [test_mutation]