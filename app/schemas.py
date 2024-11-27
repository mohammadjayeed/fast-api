from pydantic import BaseModel, EmailStr
import datetime
class PostBase(BaseModel):
    title : str
    content: str
    published: bool = True

class PostCreateUpdate(PostBase):
    pass


class PostResponse(PostBase):
    id : int
    created_at : datetime.datetime

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserCreateResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime.datetime

class UserLogin(BaseModel):
    email: EmailStr
    password : str