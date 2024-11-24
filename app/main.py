from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv
import sys

app = FastAPI()

# fastapi works its way down the first match

# function, decorator, http method and path

class Post(BaseModel):
    title : str
    content: str
    published: bool = True

def load_env_variables():
    load_dotenv(override=True)  # Reloads the .env file and overrides existing values

    host = os.getenv("HOST")
    database = os.getenv("DATABASE")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")

    return host, database, user, password


host,database,user,password = load_env_variables()


    
try:
    conn = psycopg2.connect(host=host, 
                            database=database, 
                            user=user,
                            password=password
                            ,cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection was successful")

except Exception as error:
    print("connection failed ",error)
    sys.exit(1)
        

blog_posts = [{
    'id':1,
    'title':'title 1',
    'content':'content 1'

},
    {
    'id':2,
    'title':'title 2',
    'content':'content 2'

}
]



def find_post(id):
    for i,p in enumerate(blog_posts):
        if p['id'] == id:
            print('True')
            return p,i
    return None, None


@app.get("/")  
def root():  # try to be descriptive
    return {"message":"hello world fastapi"}



@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts ORDER BY id ASC""")
    posts = cursor.fetchall()
    return {"data":posts}


# each model has a method called .dict
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(posts: Post):
    # post = posts.model_dump()
    # post['id'] = randrange(0,10000)
    # blog_posts.append(post)

    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (posts.title, posts.content, posts.published) )
    new_post = cursor.fetchone()
    conn.commit()

    return {'data':new_post}


@app.get('/posts/{id}') #path parameters are usually strings
def get_post(id:int):  # type hinting in action ?
    # post,index = find_post(id)
    

    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)

    return {'post_detail':post}


@app.put('/posts/{id}',status_code=status.HTTP_200_OK)
def update_post(id:int, posts:Post): 


    cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",(posts.title, posts.content, posts.published,str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)

    conn.commit()

    return {'data':posts}

        

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int): 
    # _,index = find_post(id)
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)
    conn.commit()

    
