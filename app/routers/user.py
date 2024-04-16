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



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user_exists = db.query(models.User).filter(models.User.email == user.email).first()

    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User with email: {user.email} already exists.')

    user.password = pwd.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
