from fastapi import status, HTTPException, Depends, APIRouter
from ..schemas import schemas
from ..DB.db_connection import get_db
from sqlalchemy.orm import Session
from ..DB import models
from ..controllers import password_utils as pwd


router = APIRouter(
    prefix = "/api/v1/users",
    tags = ['Users']
)


# Route to create a user
# This route contains a dependency injection that establishes a connection to the database (I have used postgres here)
# Schemas for the input output are clearly defined (refer schemas.py in schemas folder)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Query the user matching the email to make sure if account already exists with that email
    user_exists = db.query(models.User).filter(models.User.email == user.email).first()

    # If so, return 409 user already exists with this email
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User with email: {user.email} already exists.')

    # Else we hash the password
    user.password = pwd.hash(user.password)
    # And add the data to our Users table
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the data of new user (without password)
    return new_user
