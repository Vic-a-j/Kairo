from kairo.mutation import Filter, Mutation


def test_mutate_applies_filter():
    request = {"foo": {"bar": 1, "baz": 2}}
    filter_obj = Filter(path="foo.bar", to_value="foo.baz")
    mutation = Mutation(filter_obj)
    mutated = mutation.mutate(request.copy())
    
    assert mutated["foo"]["bar"] == 2

def test_mutate_path_not_found():
    request = {"foo": {"bar": 1}}
    filter_obj = Filter(path="foo.baz", to_value="foo.bar")
    mutation = Mutation(filter_obj)

    try:
        mutation.mutate(request.copy())
    except ValueError as e:
        assert "Expected ValueError for invalid path" in str(e)