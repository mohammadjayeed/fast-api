from pydantic import BaseModel, EmailStr
import datetime
from .models import User

class PostBase(BaseModel):
    title : str
    content: str
    published: bool = True
    # owner_id : int 

class PostCreateUpdate(PostBase):
    pass


class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserCreateResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime.datetime


class PostResponse(PostBase):
    id : int
    created_at : datetime.datetime
    owner_id : int
    owner : UserCreateResponse

class UserLogin(BaseModel):
    email: EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
    email: EmailStr
    id: int
