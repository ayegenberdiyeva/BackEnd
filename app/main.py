from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None

while True:    
    try:
        conn = psycopg.connect(host='localhost', dbname='Fastapi', user='aminayegenberdiyeva', password='yegnbb', row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(5)

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate (my_posts):
        if p["id"] == id:
            return i
    return -1

@app.get("/")
def root():
    return {"message": "Hello//"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    cursor.execute("""INSERT INTO post (title, content, status, post_rating) values (%s, %s, %s, %s) RETURNING * """, 
                   (new_post.title, new_post.content, new_post.publish, new_post.rating))
    created_post = cursor.fetchone()
    conn.commit()
    return {"data": created_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * from post WHERE post_id = %s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id - {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id - {id} was not found"}
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE post_id = %s returning  *""", (id,))
    deleting_post = cursor.fetchone()
    conn.commit()
    if deleting_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id - {id} is not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, upost: Post):
    params = [upost.title,upost.publish, id]
    if upost.content == "":
        update_query = """UPDATE post SET title = %s, status = %s WHERE post_id = %s RETURNING *"""
    else:
        params.insert(1, upost.content)
        update_query = """UPDATE post SET title = %s, content = %s, status = %s WHERER post_id = %s RETURNING *"""

    cursor.execute(update_query, params)
    updating_post = cursor.fetchone()
    conn.commit()
    if updating_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id - {id} is not found")

    return {"data": updating_post}

#2:24:47 
#2:45:02 