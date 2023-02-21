from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange



app = FastAPI()

# Create a class for validation == schema validation
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Optional for user to specify in the post request and it will default to true if not speccified
    rating: Optional[int] = None # full optional field

# a global variable to store the dictionary posts
my_posts = [{'title': 'title of a post 1', 'content': 'content of post 1', 'id': 1}, {'title': 'Favorite food', 'content': 'I like Schnizel', 'id': 2}]

def find_posts(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_index_posts(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index

########### PATH OPERATION / ROUTE ###########


@app.get("/")
def root():
    return {"message": "Welcome to my API!!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# create a post. print(post.dict() # sending back a dictionary which is a feature supported by pydantic
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
