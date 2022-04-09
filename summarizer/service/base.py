from typing import Literal
from pydantic import BaseModel

class Command(BaseModel):
    type: Literal
    class Config:
        extra = "forbid"
