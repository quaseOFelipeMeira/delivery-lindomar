from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from typing import List

from sqlalchemy.orm import Session

from core.schemas import ProductSchema, AccountSchema
from core.models import Product
from core.database import get_db
from core.authentication import get_current_user
from core.authorization import is_user


router = APIRouter(
    tags=["Product"],
    prefix="/product",
)


@router.get("", response_model=List[ProductSchema])
def get_products(
    db: Session = Depends(get_db),
    user: AccountSchema = Depends(get_current_user),
):
    """Method to get all the products

    Args:
        db (Session, optional): database session
        user (AccountSchema, optional): jwt access token on the header

    Returns:
        List[ProductSchema]: all products
    """
    if is_user(user):
        products = db.query(Product).all()
        if products:
            return products
        else:
            return []


@router.get("/{id}", response_model=ProductSchema)
def get_product(
    id: int,
    db: Session = Depends(get_db),
    user: AccountSchema = Depends(get_current_user),
):
    """Method to get a single product

    Args:
        id (int): id of the product
        db (Session, optional): database session
        user (AccountSchema, optional): jwt access token on the header

    Raises:
        HTTPException: Product not founded

    Returns:
        ProductSchema: data from the specific product
    """
    if is_user(user):
        product = db.query(Product).filter(Product.id == id).first()
        if product:
            return product
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_product(
    request: ProductSchema,
    db: Session = Depends(get_db),
    user: AccountSchema = Depends(get_current_user),
):
    """Method to create a new product

    Args:
        id (int): id of the product
        db (Session, optional): database session
        user (AccountSchema, optional): jwt access token on the header

    Returns:
        request: all data gave on param
    """
    if is_user(user):
        request.price = round(request.price, 2)
        new_product = Product(
            name=request.name,
            description=request.description,
            price=request.price,
        )
        db.add(new_product)
        db.commit()
        return request


@router.put("/{id}")
def update_product(
    id: int,
    request: ProductSchema,
    db: Session = Depends(get_db),
    user: AccountSchema = Depends(get_current_user),
):
    """Method to update a product

    Args:
        id (int): product id
        request (ProductSchema): data to overwrite the current product
        db (Session, optional): database session
        user (AccountSchema, optional): jwt access token on the header

    Raises:
        HTTPException: Product not found

    Returns:
        request: data gave on param
    """
    if is_user(user):
        product = db.query(Product).filter(Product.id == id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        product.update(request.model_dump())
        db.commit()
        return request


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    user: AccountSchema = Depends(get_current_user),
):
    """Method to delete a product

    Args:
        id (int): product id
        db (Session, optional): database session
        user (AccountSchema, optional): jwt access token on the header

    Raises:
        HTTPException: Product not founded

    Returns:
        str: "Product Removed"
    """
    if is_user(user):
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="no product with this iD"
            )

        db.delete(product)
        db.commit()
        return {"Product Removed"}
