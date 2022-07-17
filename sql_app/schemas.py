from typing import Union

import datetime as datetime
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    price: float


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    datetime: datetime.datetime

    class Config:
        orm_mode = True