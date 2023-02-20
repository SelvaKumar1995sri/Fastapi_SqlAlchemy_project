from typing import List, Optional
import datetime
from pydantic import BaseModel


class ItemBase(BaseModel):
    product: str
    seller: str
    price : float
    location: str
    categories: str
  


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    date: Optional[datetime.datetime]

    class Config:
        orm_mode = True


