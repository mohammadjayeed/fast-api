from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


# function, decorator, http method and path

class Post(BaseModel):
    title : str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")  
def root():  # try to be descriptive
    return {"message":"hello world fastapi"}



@app.get("/posts")
def get_posts():
    # logic
    return {"data":"This is your posts"}


# each model has a method called .dict
@app.post('/posts')
def create_posts(payload: Post):
    print(payload)
    print(payload.model_dump())
    return {'data':f"{payload.title} {payload.published}"}
