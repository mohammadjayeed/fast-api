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


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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



@app.get("/posts",  response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts

    # cursor.execute(""" SELECT * FROM posts ORDER BY id ASC""")
    # posts = cursor.fetchall()


# each model has a method called .dict
@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model= schemas.PostResponse )
def create_posts(posts: schemas.PostCreateUpdate, db: Session = Depends(get_db)):

    new_post = models.Post(**posts.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


    # post = posts.model_dump()
    # post['id'] = randrange(0,10000)
    # blog_posts.append(post)

    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (posts.title, posts.content, posts.published) )
    # new_post = cursor.fetchone()
    # conn.commit()



@app.get('/posts/{id}',response_model= schemas.PostResponse) # path parameters are usually strings
def get_post(id:int, db: Session = Depends(get_db)):  # type hinting in action ?
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)

    return post
    
    
    # post,index = find_post(id)
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()


@app.put('/posts/{id}',status_code=status.HTTP_200_OK, response_model= schemas.PostResponse)
def update_post(id:int, posts:schemas.PostCreateUpdate,  db: Session = Depends(get_db)): 

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)


    post_query.update(posts.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()

    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",(posts.title, posts.content, posts.published,str(id)))
    # post = cursor.fetchone()
        

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)): 

    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)
    
    post.delete(synchronize_session=False)
    db.commit()

    # _,index = find_post(id)
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()
    


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model= schemas.UserCreateResponse )
def create_users(users: schemas.UserCreate, db: Session = Depends(get_db)):

    users.password = hash(users.password)
    new_user = models.User(**users.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model= schemas.UserCreateResponse )
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)
    

    return user