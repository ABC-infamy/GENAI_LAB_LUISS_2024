from sqlmodel import SQLModel, Session, create_engine
from contextlib import contextmanager
from .config import get_settings
from models.User import Prediction, Transaction, User
from auth.hash_password import HashPassword
from services import user
from fastapi import Depends

#print(f"connecting to a database with the URL: {get_settings().DATABASE_URL_psycopg}")

engine = create_engine(
    url=get_settings().DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

def get_session():
    with Session(engine) as session:
        return session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    #lets make admin
    user.create_user(User(username = "admin", email = "admin", password = HashPassword().create_hash("admin"), balance = 10000, is_admin = 1), Session(engine))
