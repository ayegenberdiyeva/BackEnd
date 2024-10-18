from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message": "Hello//"}

@app.get("/posts")
def get_posts():
    return {"data": "posts"}

@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post)
    print(new_post.model_dump())
    return {"data": new_post}
# title str, content str 