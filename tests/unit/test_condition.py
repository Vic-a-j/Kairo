from kairo.condition import Condition, Match


def test_matches_true():
    match = Match(path="foo.bar", with_value=42)
    condition = Condition(match)
    request = {"foo": {"bar": 42}}

    assert condition.matches(request)

def test_matches_false():
    match = Match(path="foo.bar", with_value=99)
    condition = Condition(match)
    request = {"foo": {"bar": 42}}
    
    assert not condition.matches(request)

def test_matches_path_not_found():
    match = Match(path="foo.baz", with_value=42)
    condition = Condition(match)
    request = {"foo": {"bar": 42}}
    
    assert not condition.matches(request)
