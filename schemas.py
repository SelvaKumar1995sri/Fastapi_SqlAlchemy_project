from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class ItemBase(BaseModel):
    product: str
    seller: str
    price : float
    date: Optional[datetime]
    location: str
    categories: str
  


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    date: Optional[datetime]

    class Config:
        orm_mode = True


def list_serializer(prd_list):
    return [product for product in prd_list]

class product_list(BaseModel):
    data : List [ItemBase]