from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv
import sys
from .utils import load_env_variables, hash
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import auth, post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# fastapi works its way down the first match
# function, decorator, http method and path

    
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
        

@app.get("/")  
def root():  # try to be descriptive
    return {"message":"hello world fastapi"}




    


