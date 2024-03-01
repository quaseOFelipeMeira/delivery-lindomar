from fastapi import APIRouter, status, Response, HTTPException
from fastapi.params import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from core.database import get_db
from core.schemas import UserSchema, UserResponseSchema
from core.models import UserModel
from core.auth import get_current_user

router = APIRouter(
    tags=["User"],
    prefix="/user",
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseSchema,
)
def create_user(request: UserSchema, db: Session = Depends(get_db)):

    # Verifying if the email is already been used:
    account = db.query(UserModel).filter(UserModel.email == request.email).first()
    if account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email already registered.",
        )

    # hashing password
    hashed_password = pwd_context.hash(request.password)

    # adding into the database
    new_user = UserModel(
        name=request.name,
        email=request.email,
        password=hashed_password,
        role=request.role,
    )
    db.add(new_user)
    db.commit()

    return new_user


@router.get(
    "",
    response_model=UserResponseSchema,
)
def get_me(
    user: UserSchema = Depends(get_current_user),
):
    return user
