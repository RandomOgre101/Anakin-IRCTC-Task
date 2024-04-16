from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..schemas import schemas
from ..DB.db_connection import get_db
from ..DB import models
from ..controllers import password_utils as pwd
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os



load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY")

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=str(id))
    
    except JWTError:
        raise credentials_exception
    
    return token_data
    
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token[:len(token) - len(ADMIN_API_KEY)] if len(token) > 130 else token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user


def verify_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    if not ( token[::-1][:len(ADMIN_API_KEY)][::-1] == ADMIN_API_KEY ):
        return credentials_exception
         
    admin = db.query(models.User).filter(models.User.id == 1).first()

    return admin
        