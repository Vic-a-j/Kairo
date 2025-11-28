import pytest
from test_utils import get_file_path, load_to_json

from kairo import Kairo


@pytest.mark.parametrize(
    ("file_path", "override"), [
        (
            "test_canaries",
            False,
        ),
        (
            "test_override_config",
            True,
        ),
        (
            "test_no_matches",
            False,
        ),
        (
            "test_no_mutations",
            False,
        )
    ])
def test_canary_evaluate(file_path, override):
    kairo = Kairo()
    yaml_config, expected, request = get_file_path(file_path)
    kairo.load_from_yaml(yaml_config)

    # Request to json
    request = load_to_json(request)

    # Expected to json
    expected_output = load_to_json(expected)

    # Run Kairo
    actual_output = kairo.run(request, override=override)
    
    assert expected_output == actual_output


@pytest.mark.parametrize(
    ("canary_config"), [
        (
            [
                {
                    "name": "test_canary",
                    "condition": {
                        "match": {
                            "path": None,
                            "with_value": None
                        }
                    },
                    "mutations": [
                        {
                            "filter": {
                                "path": None,
                                "to_value": None
                            }
                        }
                    ],
                    "config": None
                }
            ]
        ),
        (
            [
                {
                    "name": "test_canary",
                    "condition": {
                        "match": {
                            "path": "request.header",
                            "with_value": "request.headers[?!(contains(['NO_HEADER_1', 'NO_HEADER_2'], no_val))]"
                        }
                    },
                    "mutations": [
                        {
                            "filter": {
                                "path": "request.fields",
                                "to_value": "request.fields[?fieldMetaData[?name=='dlCommercialModelCategory' && value == '89']]"
                            }
                        }
                    ],
                    "config": {"test": float("inf")}
                }
            ]
        ),
    ])
def test_create_canaries(canary_config):
    kairo = Kairo()
    kairo.create_canaries(canary_config)

    # assert values
    for idx, canary in enumerate(kairo.canaries):
        test_canary = canary_config[idx]

        assert canary.name == test_canary["name"]
        assert canary.condition.match.path == test_canary["condition"]["match"]["path"]
        assert canary.condition.match.with_value == test_canary["condition"]["match"]["with_value"]
        assert len(canary.mutations) == len(test_canary["mutations"])
        assert canary.config == test_canary["config"]