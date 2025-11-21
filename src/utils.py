import yaml
import json

def get_yaml_data(yaml_path: str) -> dict:
    with open(yaml_path, "r") as file:
        data = yaml.safe_load(file)
    return data

def get_json_data(json_str: str) -> dict:
    return json.loads(json_str)