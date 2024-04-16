from fastapi import status, HTTPException, Depends, APIRouter
from ..controllers import oauth2
from sqlalchemy.orm import Session
from ..DB.db_connection import get_db
from ..DB import models
from ..schemas import schemas



router = APIRouter(
    prefix = "/api/v1/admin",
    tags = ['Admin']
)


# ADMIN route to get all bookings
# This route contains a dependency injection that establishes a connection to the database (I have used postgres here)
# This route contains a dependency injection to make sure only admin can access this route
# Schemas for the input output are clearly defined (refer schemas.py in schemas folder)
@router.get("/bookings")
def admin_get_all_bookings(admin = Depends(oauth2.verify_admin), db: Session = Depends(get_db)):
    
    # If the request is not of admin's, return 403 unauthorized access
    try:
        if not admin.id == 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Access")  
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Access")    

    # Query all bookings that have been made by all users
    all_bookings = db.query(models.Booking).all()

    # Return the bookings
    return all_bookings



# ADMIN route to create a train route
# This route contains a dependency injection that establishes a connection to the database (I have used postgres here)
# This route contains a dependency injection to make sure only admin can access this route
# Schemas for the input output are clearly defined (refer schemas.py in schemas folder)
@router.post("/train", response_model=schemas.TrainCreateOut)
def admin_create_route(train_data: schemas.TrainCreate, admin = Depends(oauth2.verify_admin), db: Session = Depends(get_db)):

    # If the request is not of admin's, return 403 unauthorized access
    try:
        if not admin.id == 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Access")  
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Access")  

    # Else if all is correct, add the data to Trains database
    new_train = models.Train(**train_data.model_dump())
    db.add(new_train)
    db.commit()
    db.refresh(new_train)

    # Return the data of newly added train
    return new_train



# ADMIN route to modify a train route's details
# This route contains a dependency injection that establishes a connection to the database (I have used postgres here)
# This route contains a dependency injection to make sure only admin can access this route
# Schemas for the input output are clearly defined (refer schemas.py in schemas folder)
@router.put("/train/{train_id}", response_model=schemas.TrainCreateOut)
def modify_train_details(train_id: int, train_data: schemas.TrainCreate, admin = Depends(oauth2.verify_admin), db: Session = Depends(get_db)):

    # If the request is not of admin's, return 403 unauthorized access
    try:
        if not admin.id == 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Access")  
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Access")  

    # Query the train with the train_id that is passed in as query parameter
    train_query = db.query(models.Train).filter(models.Train.id == train_id)
    train = train_query.first()

    # If such a train doesnt exist, return 404 train not found
    if not train:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Train with id: {train_id} does not exist.")

    # Else update the row of data in Trains database
    train_query.update(train_data.model_dump(), synchronize_session=False)
    db.commit()

    # Return the data that was updated
    return train_query.first()