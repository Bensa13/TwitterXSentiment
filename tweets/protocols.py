from typing import Protocol
from dataclasses import dataclass


@dataclass
class TwitterAccessTokenHandler(Protocol):
    access_token: str
    access_token_secret: str
