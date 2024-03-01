from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Depends
from typing import List

from sqlalchemy.orm import Session

from core.schemas import OrderSchema, AccountSchema
from core.models import Order, OrderItem, Product, Account
from core.database import get_db
from core.authentication import get_current_user

router = APIRouter(
    tags=["Order"],
    prefix="/order",
)


@router.post("")
def login(
    request: OrderSchema,
    db: Session = Depends(get_db),
    user: AccountSchema = Depends(get_current_user),
):

    transport = db.query(Account).filter(Account.id == request.transport_id).first()
    if not transport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transport Company not founded",
        )

    # Creating new order
    new_order = Order(
        user_id=user.id,
        transport_id=transport.id,
    )
    db.add(new_order)
    db.commit()

    total_price = 0

    # for each item in list, create an item related to the order
    for item_id in request.items_id:

        prod = db.query(Product).filter(Product.id == item_id).first()

        if not prod:
            # if item not founded, the order needs to be canceled,
            # so need to delete the newest order

            order = db.query(Order).filter(Order.id == id).first()
            db.delete(order)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product not founded with id {item_id}",
            )

        total_price += prod.price

        order_item = OrderItem(
            product_id=prod.id,
            order_id=new_order.id,
        )
        db.add(order_item)

    new_order.total_price = total_price
    db.commit()
