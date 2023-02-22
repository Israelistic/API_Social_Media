import fastapi
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

# get the posts
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

# The order of the routes matter. If the lastest path was under the post{id}-rotute it will be confuesd by a different route
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"detail": post}

# The id in the route is path parameter
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id) # Since ID is str I converted it to interger so the find_post functuin can handle it.
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # Deleting post
    # Find the index in the array that has required ID
    # my_post.pop(index)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    post_dict = post.to_dict() # Convert to dictionary
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}
