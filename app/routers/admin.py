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


@router.get("/bookings")
def admin_get_all_bookings(admin = Depends(oauth2.verify_admin), db: Session = Depends(get_db)):
    
    if not admin.id == 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Access")        

    all_bookings = db.query(models.Booking).all()

    return all_bookings



@router.post("/train", response_model=schemas.TrainCreateOut)
def admin_create_route(train_data: schemas.TrainCreate, admin = Depends(oauth2.verify_admin), db: Session = Depends(get_db)):

    try:
        if not admin.id == 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Access")  
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Access")  


    new_train = models.Train(**train_data.model_dump())
    db.add(new_train)
    db.commit()
    db.refresh(new_train)

    return new_train



@router.put("/train/{train_id}", response_model=schemas.TrainCreateOut)
def modify_train_details(train_id: int, train_data: schemas.TrainCreate, admin = Depends(oauth2.verify_admin), db: Session = Depends(get_db)):

    try:
        if not admin.id == 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Access")  
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Access")  

    train_query = db.query(models.Train).filter(models.Train.id == train_id)
    train = train_query.first()

    if not train:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Train with id: {train_id} does not exist.")

    train_query.update(train_data.model_dump(), synchronize_session=False)
    db.commit()

    return train_query.first()