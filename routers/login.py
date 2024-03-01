from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import Account
from core.auth import generate_token
from core.schemas import LoginSchema

router = APIRouter(
    tags=["Auth"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login(
    # request:  OAuth2PasswordRequestForm = Depends(),
    request: LoginSchema,
    db: Session = Depends(get_db),
):
    user = db.query(Account).filter(Account.email == request.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found/invalid",
        )

    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )
    access_token = generate_token(
        data={
            "id": user.id,
            "sub": user.name,
        }
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}
