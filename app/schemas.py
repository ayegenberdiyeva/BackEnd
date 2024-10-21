from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    status: bool = True
    # rating: Optional[int] = None

class PostBase(BaseModel):
    title: str
    content: str
    status: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass