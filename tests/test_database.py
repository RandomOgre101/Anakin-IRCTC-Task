
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.DB.db_connection import get_db, Base
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
import pytest



load_dotenv()

DATABASE_HOSTNAME = os.environ.get("DATABASE_HOSTNAME")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")

SQLALCHEMY_DATABASE_URL = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}_Test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope='module')
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
