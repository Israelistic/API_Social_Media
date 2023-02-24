import fastapi
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
# from psycopg2.extras import RealDictCursor


app = FastAPI()

# Create a class for validation == schema validation
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Optional for user to specify in the post request and it will default to true if not speccified

# connection to the database.
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        # with psycopg.connect("host=localhost dbname=fastapi user=postgres") as conn:
        #     with conn.cursor() as cur:       
        print("Database connection was succesfull!")       
        break
    except Exception as error:
        print("connection to database failed")
        print("Error:", error)
        time.sleep(2)
        

# a global variable to store the dictionary posts
my_posts = [{'title': 'title of a post 1', 'content': 'content of post 1', 'id': 1}, {'title': 'Favorite food', 'content': 'I like Schnizel', 'id': 2}]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index

########### PATH OPERATION / ROUTE ###########

# root site
@app.get("/")
def root():
    return {"message": "Welcome to my API!!"}

# get the posts from the database
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

# create a post. # and commit the changes to the database.
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published)) # the %s prevents sql injection
    new_post = cursor.fetchone() 
    conn.commit() # commit the changes to the database
    return {"data": new_post}

# The order of the routes matter. If the lastest path was under the post{id}-rotute it will be confuesd by a different route
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"detail": post}

# The id in the route is path parameter
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id= %s """, (str(id)))
    post = cursor.fetchone()               
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone() # saved the deleted post
    conn.commit() # commit the changes to the database
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title= %s, content= %s, published = %s WHERE id = %s RETURNING*""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit() # commit the changes to the database
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    return {'data': updated_post}
