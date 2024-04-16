from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import admin, user, user_booking, auth
from .DB.db_connection import engine
from .DB import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(admin.router)
app.include_router(user.router)
app.include_router(user_booking.router)
app.include_router(auth.router)


@app.get("/test")
def test():
    return {"Hello": "world"}