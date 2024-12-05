from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>/'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL) # responsible for establishing connection

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# host,database,user,password = load_env_variables()
# try:
#     conn = psycopg2.connect(host=host, 
#                             database=database, 
#                             user=user,
#                             password=password
#                             ,cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("database connection was successful")

# except Exception as error:
#     print("connection failed ",error)
#     sys.exit(1)