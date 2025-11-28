import pytest

from kairo.canary import Canary
from kairo.main import Kairo


@pytest.fixture
def dummy_canary():
    return Canary("test_canary")


def test_add_canary(dummy_canary):
    kairo = Kairo()
    kairo.add_canary(dummy_canary)

    assert kairo.canaries == [dummy_canary]


def test_load_from_yaml(monkeypatch):
    sample_yaml = {
        "global_config": {
            "canaries": [
                {"name": "yaml_canary"}
            ]
        }
    }
    def fake_get_yaml_data(path):
        return sample_yaml

    monkeypatch.setattr("kairo.main.get_yaml_data", fake_get_yaml_data)
    kairo = Kairo()
    kairo.load_from_yaml("dummy_path.yaml")

    assert any(c.name == "yaml_canary" for c in kairo.canaries)


def test_load_from_json(monkeypatch):
    sample_json = {
        "global_config": {
            "canaries": [
                {"name": "json_canary"}
            ]
        }
    }
    def fake_get_json_data(json_str):
        return sample_json

    monkeypatch.setattr("kairo.main.get_json_data", fake_get_json_data)
    kairo = Kairo()
    kairo.load_from_json("{}")
    
    assert any(c.name == "json_canary" for c in kairo.canaries)