import os
from dotenv import load_dotenv
from passlib.context import CryptContext


def load_env_variables():
    load_dotenv(override=True)  # Reloads the .env file and overrides existing values

    host = os.getenv("HOST")
    database = os.getenv("DATABASE")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")

    return host, database, user, password


def hash(password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def verify(entered_password: str, password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(entered_password, password)