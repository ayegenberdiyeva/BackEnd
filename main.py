from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

@app.get("/")
def root():
    return {"message": "Hello//"}

@app.get("/posts")
def get_posts():
    return {"data": "posts"}

@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post.title)
    return {"data": "new post"}
# title str, content str 