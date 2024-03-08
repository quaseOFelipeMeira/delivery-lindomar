from fastapi import APIRouter
from . import account, login, order, product


router = APIRouter(prefix="/api/v1")

router.include_router(account.router)
router.include_router(login.router)
router.include_router(order.router)
router.include_router(product.router)