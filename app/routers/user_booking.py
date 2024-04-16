from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..schemas import schemas
from ..DB.db_connection import get_db
from ..controllers import oauth2
from datetime import datetime
from ..DB import models
from typing import List
from datetime import datetime


router = APIRouter(
    prefix = "/api/v1/user/booking",
    tags = ['User Bookings']
)



@router.get('/train', response_model=List[schemas.TrainSearchOut])
def get_seat_availability(train_data: schemas.TrainSearch, db: Session = Depends(get_db)):

    trains = db.query(models.Train).\
        filter(models.Train.start == train_data.start, 
               models.Train.end == train_data.end,
               models.Train.departing_at > datetime.now()).all()

    if not trains:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No trains are running from {train_data.start} to {train_data.end}.")

    return trains

    

@router.post("/book", status_code=status.HTTP_201_CREATED, response_model=schemas.TicketBookOut)
def book_ticket(ticket: schemas.TicketBook, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # Check if a transaction is already started
    if not db.in_transaction():
        # Start a new transaction only if there isn't one already
        transaction = db.begin()
    else:
        # Use the existing transaction
        transaction = None

    try:
        train_query = db.query(models.Train).filter(models.Train.id == ticket.train_no).with_for_update()
        train = train_query.first()

        if not train:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Train with id: {ticket.train_no} does not exist.")
        
        if ( train.seats == 0 or 
             train.seats - ticket.tickets < 0
            ):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Train with id: {ticket.train_no} does not have enough seats.")
        
        if train.departing_at < datetime.now():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Train with id: {ticket.train_no} has departed.")

        new_ticket = models.Booking(user_id=current_user.id, **ticket.model_dump())
        db.add(new_ticket)
        train_query.update({'seats': models.Train.seats - ticket.tickets}, synchronize_session='fetch')

        # If a new transaction was started, commit it
        if transaction is not None:
            transaction.commit()

    except:
        # If a new transaction was started, roll it back on error
        if transaction is not None:
            transaction.rollback()
        raise

    # Refresh or further operations with `new_ticket` can be done here, after ensuring the transaction is committed
    return new_ticket


@router.get("/{booking_id}")
def get_booking_details(booking_id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    booking_query = db.query(models.Booking).filter(models.Booking.id == booking_id)
    booking = booking_query.first()

    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with id: {booking_id} does not exist.")
    
    if booking.user_id != current_user.id and current_user.id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    return booking