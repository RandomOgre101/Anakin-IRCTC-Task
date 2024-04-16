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


# Route for user to get information on trains from destination A to destination B
# This route contains a dependency injection that establishes a connection to the database (I have used postgres here)
# Schemas for the input output are clearly defined (refer schemas.py in schemas folder)
@router.post('/train', response_model=List[schemas.TrainSearchOut])
def get_seat_availability(train_data: schemas.TrainSearch, db: Session = Depends(get_db)):

    # Query all trains going from A to B
    # Edge case: There may be trains in the DB that have already departed
    #            So I added a condition to make sure the departing time
    #            of the trains to be shown are after the time now
    trains = db.query(models.Train).\
        filter(models.Train.start == train_data.start, 
               models.Train.end == train_data.end,
               models.Train.departing_at > datetime.now()).all()

    # Exception Handling: If there are no trains that match the conditions, return 404 no trains found
    if not trains:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No trains are running from {train_data.start} to {train_data.end}.")

    # Or return the trains and their info
    return trains



# Route to book tickets for a train
# This route contains a dependency injection that establishes a connection to the database (I have used postgres here)
# This route contains a dependency injection that makes sure only logged in user with valid JWT can access the route
# Schemas for the input output are clearly defined (refer schemas.py in schemas folder)
#       *** The assignment told me to handle race conditions which are done below ***
@router.post("/book", status_code=status.HTTP_201_CREATED, response_model=schemas.TicketBookOut)
def book_ticket(ticket: schemas.TicketBook, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # Exception Handling: Check if a DB transaction has already started
    if not db.in_transaction():
        # Start a new transaction only if is not there already
        transaction = db.begin()
    else:
        # Or else use the existing transaction
        transaction = None


    try:
        # Query the train which has the same id as the one passed in
        # with_for_update() locks the DB row, which ensures two users cannot book at the same time
        train_query = db.query(models.Train).filter(models.Train.id == ticket.train_no).with_for_update()
        train = train_query.first()

        # Exception Handling: If train with passed in id doesnt exist, return 404 train doesnt exist 
        if not train:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Train with id: {ticket.train_no} does not exist.")
        
        # Edge case: If the train has no seats left or if the number of tickets about
        #            to be booked are more than the seats left in train,
        #            return a 403 train doesnt have enough seats
        if ( train.seats == 0 or 
             train.seats - ticket.tickets < 0
            ):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Train with id: {ticket.train_no} does not have enough seats.")
        
        # Edge case: If the train has already departed, return 403 train has already departed
        if train.departing_at < datetime.now():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Train with id: {ticket.train_no} has departed.")

        # If all conditions are passed, book the tickets and add the data to Booking table
        new_ticket = models.Booking(user_id=current_user.id, **ticket.model_dump())
        db.add(new_ticket)
        # Update the seats on the train, minusing by however much tickets were booked
        train_query.update({'seats': models.Train.seats - ticket.tickets})
        db.commit()

    except:
        # If a new transaction was started then we can roll it back on error
        if transaction is not None:
            transaction.rollback()
        raise

    # Return the ticket data
    return new_ticket



# Route to get booking details of a specifc booking from the booking_id that is passed in query paramters
# This route contains a dependency injection that establishes a connection to the database (I have used postgres here)
# This route contains a dependency injection that makes sure only logged in user with valid JWT can access the route
# Schema for the output is clearly defined (refer schemas.py in schemas folder)
@router.get("/{booking_id}", response_model=schemas.BookingDetailsOut)
def get_booking_details(booking_id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # Query to get the data of booking details with the passed in booking id
    booking_query = db.query(models.Booking).filter(models.Booking.id == booking_id)
    booking = booking_query.first()

    # If such a record doesnt exist, then return 404 booking not found
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with id: {booking_id} does not exist.")
    
    # If the user who is logged in does not match the booking's owner
    # and is not admin, return 403 not authorized
    if booking.user_id != current_user.id and current_user.id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    # Return the booking details
    return booking