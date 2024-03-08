from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Depends
from typing import List

from sqlalchemy.orm import Session

from core.models import Order, OrderItem, Product, Account
from core.database import get_db
from core.authentication import get_current_user
from core.authorization import is_user, is_transport
from core.schemas import (
    OrderSchema,
    OrderResponseSchema,
    AccountSchema,
)

router = APIRouter(
    tags=["Order"],
    prefix="/order",
)


def get_status_message(status: int):
    """Method to generate messages from the current status of the order

    Args:
        status (int): current status of the order

    Returns:
        str: message matching with the status
    """
    match status:
        case -1:
            return "order refused"
        case 0:
            return "order waiting approval"
        case 1:
            return "order approved"
        case 2:
            return "order payed"
        case 3:
            return "order in the way"
        case 4:
            return "order delivered"


@router.get("", response_model=List[OrderResponseSchema])
def get_orders(
    db: Session = Depends(get_db),
    user: AccountSchema = Depends(get_current_user),
):
    """Endpoint to get all orders, depending of the logged account role:    \n
    if the role is 'USER', can view only your orders    \n
    if the role is 'TRANSPORT', can view only orders that it can transport

    Args:
        db (Session, optional): database session
        user (AccountSchema, optional): jwt access token on the header

    Returns:
        _type_: _description_
    """

    # Verifying if the user is logged in
    if user:

        # Defying query depending of user's role:
        if user.role == "TRANSPORT":
            query = Order.transport_id
        if user.role == "USER":
            query = Order.user_id

        # Getting orders
        orders = db.query(Order).filter(query == user.id).order_by(Order.status).all()

        # Verifying the there is at least one order
        if orders:

            # getting each products, of each order:
            for order in orders:

                items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
                products = []
                for item in items:
                    product = (
                        db.query(Product).filter(Product.id == item.product_id).first()
                    )
                    products.append(product)
                order.products = products

                user = db.query(Account).filter(Account.id == order.user_id).first()
                transport = (
                    db.query(Account).filter(Account.id == order.transport_id).first()
                )

                # setting product data into the orders:
                order.user = user.name
                order.transport = transport.name
                order.status_msg = get_status_message(order.status)

            return orders
        else:
            return []


@router.get("/{id}", response_model=OrderResponseSchema)
def get_order(
    id: int,
    db: Session = Depends(get_db),
    user: AccountSchema = Depends(get_current_user),
):
    """Method to detail a single order

    Args:
        id (int): id of the order
        db (Session, optional): database session
        user (AccountSchema, optional): jwt access token on the header

    Raises:
        HTTPException: product to founded - HTTP 404

    Returns:
        order (OrderResponseSchema)
    """

    # Verifying if the user is logged
    if user:

        # Searching for the order
        order = db.query(Order).filter(Order.id == id).first()
        if order:

            # Getting all the items for this order
            items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
            products = []

            for item in items:
                product = (
                    db.query(Product).filter(Product.id == item.product_id).first()
                )
                products.append(product)

            user = db.query(Account).filter(Account.id == order.user_id).first()
            transport = (
                db.query(Account).filter(Account.id == order.transport_id).first()
            )

            order.products = products
            order.user = user.name
            order.transport = transport.name
            order.status_msg = get_status_message(order.status)
            return order

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )


@router.post("")
def new_order(
    request: OrderSchema,
    db: Session = Depends(get_db),
    user: AccountSchema = Depends(get_current_user),
):
    """Method to create new orders

    Args:
        request (OrderSchema): content of the body
        db (Session, optional): database session
        user (AccountSchema, optional): jwt access token on the header

    Raises:
        HTTPException: Transport Company not founded
        HTTPException: Product not founded

    Returns:
        _type_: _description_
    """
    if is_user(user):

        account = db.query(Account).filter(Account.id == request.transport_id).first()

        # Verifying if this ID exists and if this account is a transport company
        if not account or account.role != "TRANSPORT":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transport Company not founded",
            )

        # Creating new order
        new_order = Order(
            user_id=user.id,
            transport_id=account.id,
            status=0,
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
                    detail=f"Product not founded",
                )

            # Incrementing the price on each iteration
            total_price += prod.price

            # Saving an object to link the product and the order
            order_item = OrderItem(
                product_id=prod.id,
                order_id=new_order.id,
            )
            db.add(order_item)

        # Setting the final total price of the order
        new_order.total_price = total_price
        db.commit()
        return request


@router.patch(
    "/{id}/advance",
    # response_model=List[OrderSchema],
)
def advance_status(
    id: int,
    db: Session = Depends(get_db),
    user: AccountSchema = Depends(get_current_user),
):
    """Method to increase the status of an order

    Args:
        id (int): id of the order
        db (Session, optional): database session
        user (AccountSchema, optional): jwt access token on the header

    Returns:
        Response: http response with the current status code, and status message of the order
    """
    if is_transport(user):
        order = db.query(Order).filter(Order.id == id).first()

        if order.status >= 4 and order.status != 0:
            order.status += 1
            db.commit()

            response_msg = {
                "msg": "Order updated",
                "status": order.status,
                "status_message": get_status_message(order.status),
            }
            response_status = status.HTTP_200_OK
            return Response(content=response_msg, status_code=response_status)

        response_msg = {
            "msg": "Order status cannot be increased",
            "status": order.status,
            "status_message": get_status_message(order.status),
        }
        response_status = status.HTTP_403_FORBIDDEN
        return Response(content=response_msg, status_code=response_status)

    response_msg = {
        "msg": "only transport companies can increase",
    }
    response_status = status.HTTP_403_FORBIDDEN
    return Response(content=response_msg, status_code=response_status)


@router.patch(
    "/{id}/cancel",
    response_model=OrderSchema,
)
def advance_status(
    id: int,
    db: Session = Depends(get_db),
    user: AccountSchema = Depends(get_current_user),
):
    """Method to refuse an order

    Args:
        id (int): id of the order
        db (Session, optional): database session
        user (AccountSchema, optional): jwt access token on the header

    Returns:
        str: cancellation confirmation
    """
    if is_transport(user):
        order = db.query(Order).filter(Order.id == id).first()
        order.status = 0
        db.commit()
        response_msg = {
            "msg": "Order canceled",
        }
        response_status = status.HTTP_200_OK

        return Response(content=response_msg, status_code=response_status)
