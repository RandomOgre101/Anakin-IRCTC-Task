from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os



load_dotenv()

# Getting all the required database connection data from .env file
DATABASE_HOSTNAME = os.environ.get("DATABASE_HOSTNAME")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")

# Connection URL
SQLALCHEMY_DATABASE_URL = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}'

# SQLAlchemy engine to connect to the database using URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal class, 
#                   autocommit is False because I want to manually commit the changes after a transaction
#                   bind engine so the session is associated to the engine we created above
#                   autoflush is False so the objects are not automatically flushed before each query
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions in models.py
Base = declarative_base()

# Function to establish a DB session
def get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

