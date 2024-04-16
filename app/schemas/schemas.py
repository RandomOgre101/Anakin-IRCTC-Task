from enum import Enum
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class Roles(str, Enum):
    user = "user"
    admin = "admin"



class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class TicketBook(BaseModel):
    train_no: int
    tickets: int
class TicketBookOut(TicketBook):
    user_id: int
    created_at: datetime


class TrainSearch(BaseModel):
    start: str
    end: str

class TrainSearchOut(BaseModel):
    id: int
    seats: int
    departing_at: datetime


class TrainCreate(BaseModel):
    start: str
    end: str
    departing_at: datetime
    seats: int

class TrainCreateOut(TrainCreate):
    id: int



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None