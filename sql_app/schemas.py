from typing import Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    price: float


class ItemCreate(ItemBase):
    datetime: str


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True