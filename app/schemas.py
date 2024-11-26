from pydantic import BaseModel
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