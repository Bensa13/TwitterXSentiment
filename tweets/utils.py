from dataclasses import dataclass
import yaml
import pathlib
from dataclasses import dataclass


def load_yaml(path: pathlib.Path) -> dict[str, str]:
    # loads a yaml-file and returns it as a dictionary

    file = open(path)
    dct = yaml.safe_load(file)
    file.close()
    return dct


@dataclass
class TokenHandler:
    access_token: str
    access_token_secret: str
