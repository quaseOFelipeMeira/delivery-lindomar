from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailSyntaxError

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
    """Method to create an account into de database

    Args:
        request (AccountSchema): json with account and address data
        role (str): role of the new account
        db (Session): database session

    Raises:
        HTTPException: Password less than 6 characters
        EmailSyntaxError: Invalid email
        IntegrityError: Email duplicated (already inserted on database)

    Returns:
        request (AccountSchema): all the data received
    """

    try:
        # Validating Email
        validate_email(request.email, check_deliverability=False)

        # Validating Password
        if len(request.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters",
            )

        # Hashing password
        hashed_password = pwd_context.hash(request.password)

        # Adding user into the database
        new_user = Account(
            name=request.name,
            email=request.email,
            password=hashed_password,
            role=role,
        )
        db.add(new_user)

        # Getting the id of the last acount
        user_id = db.query(Account).order_by(Account.id.desc()).first().id

        # Adding address into the database
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

    except EmailSyntaxError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email"
        )

    except IntegrityError as e:
        message = (
            str(e.orig).split(":")[0] + ": " + str(e.orig).split(":")[1].split(".")[1]
        )
        raise HTTPException(detail=message, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(request: AccountSchema, db: Session = Depends(get_db)):
    create_account(request, "USER", db)
    return request


@router.post("/transport", status_code=status.HTTP_201_CREATED)
def create_transport(request: AccountSchema, db: Session = Depends(get_db)):
    create_account(request, "TRANSPORT", db)
    return request


@router.get("", response_model=AccountResponseSchema)
def get_me(user: AccountSchema = Depends(get_current_user)):
    return user
