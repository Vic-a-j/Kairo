import json
import os
from typing import Any


def get_file_path(file_name: str) -> tuple[str, str, str]:
    """Given file path inside data, return associated files:
    - canaries.yaml
    - expected.json
    - request.json
    """

    files = ["canaries.yaml", "expected.json", "request.json"]
    return (os.path.join(f"tests/data/{file_name}/{file}") for file in files)


def load_to_json(file_name: str) -> dict[str, Any]:
    """Load json file."""
    with open(file_name) as file:
        data = json.load(file)

    return data