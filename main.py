from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# fastapi works its way down the first match

# function, decorator, http method and path

class Post(BaseModel):
    title : str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
    # logic
    return {"data":blog_posts}


# each model has a method called .dict
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(posts: Post):
    post = posts.model_dump()
    post['id'] = randrange(0,10000)
    blog_posts.append(post)

    return {'data':posts}


@app.get('/posts/{id}') #path parameters are usually strings
def get_post(id:int):  # type hinting in action ?
    post,index = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)
    return {'post_detail':post}


@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int): 
    post,index = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)
    else:
        blog_posts.pop(index)
