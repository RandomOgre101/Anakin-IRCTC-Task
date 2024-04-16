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

# We are using the fastapi OAuth2PasswordBearer because it provides easy implementation of token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Here is the admin secret api key and all the data for our JWT
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY")


# Function to create the access token
def create_access_token(data: dict):

    # Making a copy of the data so we dont modify the original
    to_encode = data.copy()

    # I have set the expiration time of token to be 60 mins, so that is done here
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Encoding the JWT with data, secret key and algorithm (I have used HS256 in this assignment)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Return the encoded JWT
    return encoded_jwt


# Function to verify if the access token is valid
def verify_access_token(token: str, credentials_exception):

    try:
        # Get the payload data (user_id is what I have used)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract user_id
        id: str = payload.get("user_id")

        # If there is no user_id, return 401 unauthorized
        if id is None:
            raise credentials_exception
        
        # Else the token data is created with schema that is already defined
        token_data = schemas.TokenData(id=str(id))
    
    # If anything doesnt match/is invalid, return 401 unauthorized
    except JWTError:
        raise credentials_exception
    
    # Else return the token data
    return token_data
    

# Function that gets the current user from the payload data of JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    # Condition to check if it is a user JWT or admin JWT (Admin JWT has the secret key at the end)
    token = verify_access_token(token[:len(token) - len(ADMIN_API_KEY)] if len(token) > 130 else token, credentials_exception)

    # Query the user details from the user_id in payload of JWT
    user = db.query(models.User).filter(models.User.id == token.id).first()

    # Return the user details
    return user


# Function to verify if it is admin
def verify_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    # If not admin, return 401 unauthorized
    if not ( token[::-1][:len(ADMIN_API_KEY)][::-1] == ADMIN_API_KEY ):
        return credentials_exception
    
    # Query admin details
    admin = db.query(models.User).filter(models.User.id == 1).first()

    # Return the admin details
    return admin
        