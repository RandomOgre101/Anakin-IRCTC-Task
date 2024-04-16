from ..DB.db_connection import Base
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..schemas.schemas import Roles


# Here is where I have defined schemas for the databases using SQLAlchemy (ORM)



# This is the users table, it contains:
# user_id (Primary Key)
# email of user
# password of user (it will be hashed then stored)
# role of user (ENUM: admin or user)
# created_at (when the account was created)
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(Roles), nullable=False, default='user')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



# This is the trains table, it contains:
# train_id
# start (boarding station)
# end (destination station)
# departing_at (time and date of departure)
# seats (amount of seats available on train)
class Train(Base):
    __tablename__ = "trains"

    id = Column(Integer, nullable=False, primary_key=True)
    start = Column(String, nullable=False)
    end = Column(String, nullable=False)
    departing_at = Column(TIMESTAMP, nullable=False)
    seats = Column(Integer, nullable=False)



# This is the booking details table, it contains:
# booking id
# user_id (Foreign Key of user_id from users table)
# train_no (Foreign Key of train_id from trains table)
# created_at (date and time of the booking)
class Booking(Base):
    __tablename__ = "bookingDetails"

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    train_no = Column(Integer, ForeignKey('trains.id', ondelete='CASCADE'), nullable=False)
    tickets = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))