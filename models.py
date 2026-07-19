from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["Laptop"])
    description: Optional[str] = Field(None, max_length=500, examples=["A powerful laptop"])
    price: float = Field(..., gt=0, examples=[999.99])
    in_stock: bool = Field(True, examples=[True])


class ItemUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    in_stock: bool = True


class Item(ItemCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
