from fastapi import APIRouter, Depends, status, HTTPException
from ..DB.db_connection import get_db
from ..schemas import schemas
from ..DB import models
from ..controllers import password_utils as pwd, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os


router = APIRouter(
    prefix = "/api/v1",
    tags = ['Authentication'],
)


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not pwd.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY")


@router.post('/adminlogin', response_model=schemas.Token)
def admin_login(admin_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    admin_details = db.query(models.User).filter(models.User.id == 1).first()

    if (not ( admin_credentials.username == admin_details.email ) or 
        not ( pwd.verify(admin_credentials.password, admin_details.password) )
        ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": admin_details.id})

    return {"access_token": access_token + ADMIN_API_KEY, "token_type": "bearer"}