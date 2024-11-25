from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .utils import load_env_variables

host,database,user,password = load_env_variables()
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>/'

SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{host}/{database}'


engine = create_engine(SQLALCHEMY_DATABASE_URL) # responsible for establishing connection

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()