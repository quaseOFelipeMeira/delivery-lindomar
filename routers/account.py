from fastapi import APIRouter, status, Response, HTTPException
from fastapi.params import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from core.database import get_db
from core.schemas import AccountSchema, AccountResponseSchema
from core.models import Account, Address
from core.authentication import get_current_user

router = APIRouter(
    tags=["Account"],
    prefix="/account",
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_account(request: AccountSchema, role: str, db: Session):

    # hashing password
    hashed_password = pwd_context.hash(request.password)

    # adding user into the database
    new_user = Account(
        name=request.name,
        email=request.email,
        password=hashed_password,
        role=role,
    )
    db.add(new_user)
    db.commit()

    # getting the id of the last
    user_id = db.query(Account).order_by(Account.id.desc()).first().id

    # adding address into the database
    address = Address(
        account_id=user_id,
        complement=request.complement,
        street=request.street,
        house_number=request.house_number,
        neighborhood=request.neighborhood,
        city=request.city,
        state=request.state,
        CEP=request.CEP,
    )

    db.add(address)
    db.commit()

    return user_id


@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(request: AccountSchema, db: Session = Depends(get_db)):
    create_account(request, "USER", db)
    return request


@router.post("/transport", status_code=status.HTTP_201_CREATED)
def create_transport(request: AccountSchema, db: Session = Depends(get_db)):
    create_account(request, "TRANSPORT", db)
    return request


@router.get("", response_model=AccountResponseSchema)
def get_me(
    user: AccountSchema = Depends(get_current_user),
):
    return user
