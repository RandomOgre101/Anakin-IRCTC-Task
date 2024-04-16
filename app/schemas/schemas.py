from enum import Enum
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# These are the schemas to make sure all data that is given in and given out is valid and of valid types


# This is an ENUM for the Users database, to define role of user
class Roles(str, Enum):
    user = "user"
    admin = "admin"



# This is the schema for data to be received when creating a new account for a user
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# This is the schema for data to be returned when the account creation was successful
class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True



# This is the schema for data to be received when a user books a train ticket
class TicketBook(BaseModel):
    train_no: int
    tickets: int

# This is the schema for data to be returned when the ticket was successfully booked
# It inherits from class TicketBook so as not to put train_no and tickets again in the below schema
# Its a way to avoid redundant variables in schemas
class TicketBookOut(TicketBook):
    user_id: int



# This is the schema for data to be received for when a user searches for a train for seat availablilty
class TrainSearch(BaseModel):
    start: str
    end: str

# This is the schema for data to be returned for when a user searches for a train for seat availablilty
class TrainSearchOut(BaseModel):
    id: int
    seats: int
    departing_at: datetime



# This is the schema for data to be received for when the admin creates a new train route
class TrainCreate(BaseModel):
    start: str
    end: str
    departing_at: datetime
    seats: int

#This is the schema for data to be returned for when admin successfully creates a new train route
# It inherits from class TrainCreate so all data of that schema is also shown here
# Its a way to avoid redundant variables in schemas
class TrainCreateOut(TrainCreate):
    id: int



# This is the schema for data to be returned for when a user gets their booking details
class BookingDetailsOut(BaseModel):
    id: int
    user_id: int
    train_no: int
    tickets: int
    created_at: datetime



# This is the schema for the token to be returned to user
class Token(BaseModel):
    access_token: str
    token_type: str

# This is the schema for the JWT when it is decoded and the user_id is retreived from the payload
class TokenData(BaseModel):
    id: Optional[str] = None