from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Depends
from typing import List

from sqlalchemy.orm import Session

from core.schemas import ProductSchema
from core.models import ProductModel
from core.database import get_db


router = APIRouter(
    tags=["Product"],
    prefix="/product",
)


@router.get(
    "",
    response_model=List[ProductSchema],
    status_code=status.HTTP_200_OK,
)
def get_products(
    db: Session = Depends(get_db),
):
    products = db.query(ProductModel).all()
    if products:
        return products
    else:
        return []


@router.get(
    "/{id}",
    response_model=ProductSchema,
    status_code=status.HTTP_200_OK,
)
def get_product(
    id: int,
    db: Session = Depends(get_db),
):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if product:
        return product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductSchema,
)
def create_product(
    request: ProductSchema,
    db: Session = Depends(get_db),
):
    request.price = round(request.price, 2)
    new_product = ProductModel(
        name=request.name,
        description=request.description,
        price=request.price,
    )
    db.add(new_product)
    db.commit()
    return request


@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductSchema,
)
def create_product(
    id: int,
    request: ProductSchema,
    db: Session = Depends(get_db),
):
    product = db.query(ProductModel).filter(ProductModel.id == id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    product.update(request.model_dump())
    db.commit()
    return request


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    id: int,
    db: Session = Depends(get_db),
):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no product with this iD"
        )

    db.delete(product)
    db.commit()
    return {"Product Removed"}
