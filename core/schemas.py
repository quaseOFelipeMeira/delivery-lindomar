from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    role: str

    class Config:
        # orm_mode = True
        from_attributes = True


class UserResponseSchema(BaseModel):
    name: str
    email: str
    role: str

    class Config:
        # orm_mode = True
        from_attributes = True


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
