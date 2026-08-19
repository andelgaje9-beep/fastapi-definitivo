from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel 

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str 
    published: bool= True 
    

my_post = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
    {"title": "favorite food", "content": "I like pizza", "id": 2 }, 
    {"title": "tengo sueno", "content": "voy a dormir", "id": 3 }
]

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p
        
def find_index(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            print(i)  
            return i 
    return None
        
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_all_posts():
    return my_post

@app.get("/posts/{id}")
async def get_post_id(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "id not found")
    return {"post_detail": post}


# siempre debe ir en plurar el path por convencion
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.model_dump()
    print (post_dict)
    my_post.append(post_dict)
    return {"new_post": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index(id) 
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "id not found")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_index(id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )

    post_dict = post.model_dump()
    post_dict["id"] = id
    my_post[index] = post_dict

    return {"data": post_dict}
