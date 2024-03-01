from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Depends
from typing import List

from sqlalchemy.orm import Session

from core.schemas import ProductSchema
from core.models import ProductModel
from core.database import get_db

router = APIRouter(tags=["Order"], prefix="/order")


@router.post("")
def login(request: List[ProductSchema], db: Session = Depends(get_db)):
    total_price = 0
    for item in request:
        total_price += item.price

    print("total")
    print(total_price)
