from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
from . import models, schemas
from .database import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind= engine)

app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

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

# my_posts = [
#     {"title": "title of post 1", "content": "content of post 1", "id": 1},
#     {"title": "title of post 2", "content": "content of post 2", "id": 2}]

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
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO post (title, content, status, post_rating) values (%s, %s, %s, %s) RETURNING * """, 
    #                (new_post.title, new_post.content, new_post.publish, new_post.rating))
    # created_post = cursor.fetchone()
    # conn.commit()

    created_post = models.Post(**new_post.model_dump())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return {"data": created_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from post WHERE post_id = %s""", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.post_id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id - {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id - {id} was not found"}
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM post WHERE post_id = %s returning  *""", (id,))
    # deleting_post = cursor.fetchone()
    # conn.commit()
    deleting_post = db.query(models.Post).filter(models.Post.post_id == id)

    if deleting_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id - {id} is not found")
    
    deleting_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, upost: schemas.PostUpdate, db: Session = Depends(get_db)):
    # params = [upost.title,upost.publish, id]
    # if upost.content == "":
    #     update_query = """UPDATE post SET title = %s, status = %s, updated_at = current_timestamp WHERE post_id = %s RETURNING *"""
    # else:
    #     params.insert(1, upost.content)
    #     update_query = """UPDATE post SET title = %s, content = %s, status = %s, updated_at = current_timestamp WHERER post_id = %s RETURNING *"""

    # cursor.execute(update_query, params)
    # updating_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.post_id == id)

    updating_post = post_query.first()

    if updating_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id - {id} is not found")

    post_query.update(upost.model_dump(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}

#2:24:47 
#2:45:02 
#4:30:49 