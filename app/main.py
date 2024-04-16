from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import admin, user, user_booking, auth
from .DB.db_connection import engine
from .DB import models


# Create all database tables defined in models.py using the Base class
models.Base.metadata.create_all(bind=engine)

# Initializing the FastAPI app
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

# I added routers here to segregate the routes so it is easier to maintain, read and build on
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(user_booking.router)
app.include_router(auth.router)

@app.get("/")
def test():
    return {"message": "Hello World"}