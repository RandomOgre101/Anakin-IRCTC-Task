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


# Route to login, verify and generate JWT for user
# This route contains a dependency injection that establishes a connection to the database (I have used postgres here)
# Schemas for the input output are clearly defined (refer schemas.py in schemas folder)
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # Query the user by given email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # If such a user doesnt exist, return 403 invalid credentials
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # If passwords dont match, return 403, invalid credentials
    if not pwd.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Else, generate JWT (I have chosen to include the user_id in the payload, so it can be accessed in other routes easily)
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    # Return the token
    return {"access_token": access_token, "token_type": "bearer"}


ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY")

# ADMIN route to login, verify and generate JWT for admin
# This route contains a dependency injection that establishes a connection to the database (I have used postgres here)
# Schemas for the input output are clearly defined (refer schemas.py in schemas folder)
@router.post('/adminlogin', response_model=schemas.Token)
def admin_login(admin_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # Query the admin details
    admin_details = db.query(models.User).filter(models.User.id == 1).first()

    # If these conditions are not met, return 403 invalid credentials
    if (not ( admin_credentials.username == admin_details.email ) or 
        not ( pwd.verify(admin_credentials.password, admin_details.password) )
        ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Else, generate JWT (I have chosen to include the user_id in the payload here also)
    access_token = oauth2.create_access_token(data={"user_id": admin_details.id})

    # Return the token along with the secret api key that is only for admin
    return {"access_token": access_token + ADMIN_API_KEY, "token_type": "bearer"}