from typing import Any, Literal

from pydantic import BaseModel


class Command(BaseModel):
    type: Literal[None]

    class Config:
        extra = "forbid"
