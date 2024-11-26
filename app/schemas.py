from pydantic import BaseModel

class PostBase(BaseModel):
    title : str
    content: str
    published: bool = True

class PostCreateUpdate(PostBase):
    pass