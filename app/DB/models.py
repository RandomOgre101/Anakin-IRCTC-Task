from ..DB.db_connection import Base
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..schemas.schemas import Roles



class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(Roles), nullable=False, default='user')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Train(Base):
    __tablename__ = "trains"

    id = Column(Integer, nullable=False, primary_key=True)
    start = Column(String, nullable=False)
    end = Column(String, nullable=False)
    departing_at = Column(TIMESTAMP, nullable=False)
    seats = Column(Integer, nullable=False)


class Booking(Base):
    __tablename__ = "bookingDetails"

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    train_no = Column(Integer, ForeignKey('trains.id', ondelete='CASCADE'), nullable=False)
    tickets = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))