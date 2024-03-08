from fastapi import APIRouter, Depends, status, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import Account
from core.authentication import generate_token
from core.schemas import LoginSchema

router = APIRouter(
    tags=["Auth"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login(
    request: LoginSchema,
    db: Session = Depends(get_db),
):
    """Method to Login and retrieve jwt access token,

    Args:
        request (LoginSchema): json with account and address data
        db (Session, optional): database session

    Raises:
        HTTPException: User not founded - HTTP 404
        HTTPException: Invalid password - HTTP 401

    Returns:
        dict containing access token, users's id and role
    """

    # Getting the user by the email
    user = db.query(Account).filter(Account.email == request.email).first()

    # Raising exception if user == null
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found/invalid",
        )

    # Verifying if is the correct password
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )

    # Setting additional data to retrieve with the token
    access_token = generate_token(
        data={
            "id": user.id,
            "role": user.role,
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}
