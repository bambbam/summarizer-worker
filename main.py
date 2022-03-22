from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.put("/items/{item_id}")
def read_item(item_id: int, item: Item):
    return {"item_id": item_id, "item_name": item.name}
