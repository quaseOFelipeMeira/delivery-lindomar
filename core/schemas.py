from pydantic import BaseModel
from typing import Optional


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


class AccountResponseSchema(AccountSchema):
    id: int


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
