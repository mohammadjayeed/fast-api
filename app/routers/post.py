from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix = '/posts',
    tags=['posts']
)

@router.get('/',  response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts

    # cursor.execute(""" SELECT * FROM posts ORDER BY id ASC""")
    # posts = cursor.fetchall()


# each model has a method called .dict
@router.post('/', status_code=status.HTTP_201_CREATED, response_model= schemas.PostResponse )
def create_posts(posts: schemas.PostCreateUpdate, db: Session = Depends(get_db)):

    new_post = models.Post(**posts.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


    # post = posts.model_dump()
    # post['id'] = randrange(0,10000)
    # blog_posts.routerend(post)

    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (posts.title, posts.content, posts.published) )
    # new_post = cursor.fetchone()
    # conn.commit()



@router.get('/{id}',response_model= schemas.PostResponse) # path parameters are usually strings
def get_post(id:int, db: Session = Depends(get_db)):  # type hinting in action ?
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)

    return post
    
    
    # post,index = find_post(id)
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()


@router.put('/{id}',status_code=status.HTTP_200_OK, response_model= schemas.PostResponse)
def update_post(id:int, posts:schemas.PostCreateUpdate,  db: Session = Depends(get_db)): 

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)


    post_query.update(posts.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()

    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",(posts.title, posts.content, posts.published,str(id)))
    # post = cursor.fetchone()
        

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)): 

    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)
    
    post.delete(synchronize_session=False)
    db.commit()

    # _,index = find_post(id)
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()