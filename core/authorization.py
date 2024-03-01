from fastapi import HTTPException, status

from core.schemas import AccountSchema


def is_user(user: AccountSchema):
    if not user:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT)
    if user.role == "USER" or user.role == "ADMIN":
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def is_transport(user: AccountSchema):
    if not user:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT)
    if user.role == "TRANSPORT" or user.role == "ADMIN":
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
