import json
from typing import Any

import yaml


def get_yaml_data(yaml_path: str) -> Any:
    """Load YAML data from a file.

    Args:
        yaml_path (str): Path to the YAML file.

    Returns:
        Dict: Parsed YAML data.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the YAML is invalid.
    """
    try:
        with open(yaml_path, encoding="utf-8") as file:
            data = yaml.safe_load(file)
        return data
    except Exception as err:
        raise RuntimeError(f"Failed to load YAML file '{yaml_path}': {err}") from err

def get_json_data(json_str: str) -> Any:
    """Parse JSON string to Python object.

    Args:
        json_str (str): JSON string.

    Returns:
        Dict: Parsed JSON data.

    Raises:
        json.JSONDecodeError: If the JSON is invalid.
    """
    try:
        return json.loads(json_str)
    except Exception as err:
        raise RuntimeError(f"Failed to parse JSON string: {err}") from err