from pydantic import BaseModel
from typing import Optional, List


class AccountSchema(BaseModel):
    name: str
    email: str
    password: str

    complement: str
    street: str
    house_number: str
    neighborhood: str
    city: str
    state: str
    CEP: str
    # id: Optional[int] = None


class AccountResponseSchema(BaseModel):
    id: int
    name: str
    email: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


class LoginSchema(BaseModel):
    email: str
    password: str


class ProductSchema(BaseModel):
    name: str
    description: str
    price: float


class OrderSchema(BaseModel):
    items: List[int]
    transport_id: int


class OrderResponseSchema(BaseModel):
    total_price: float
    id: int
    status: int
    user: str
    transport: str
    status_msg: str
    products: List[ProductSchema]
