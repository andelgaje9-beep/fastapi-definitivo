from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import psycopg_pool 
import psycopg  

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str 
    published: bool= True 
    
    
## Connect to an existing database with connection pools
pool = psycopg_pool.ConnectionPool(
    "host=localhost dbname=fastapi user=postgres password=0624",
    min_size=1,
    max_size=10
) 


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_all_posts():
    try:
        with pool.connection() as conn:  
            with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute("SELECT * FROM posts")
                posts = cur.fetchall()
                # print(posts)
                return {"data": posts}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.get("/posts/{id}")
async def get_post_id(id: int):
    try:
        with pool.connection() as conn:  
            with conn.cursor(row_factory=psycopg.rows.dict_row) as cur: #cada fila se devuelve como un diccionario en lugar de una tupla.
                cur.execute("SELECT * FROM posts WHERE id = %s", (id,))
                post = cur.fetchone()
                
                if post is None: 
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Post con id {id} no encontrado")
                
                return post
            
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


# siempre debe ir en plurar el path por convencion
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    try:
            with pool.connection() as conn:  
                with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                    cur.execute("INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *", 
                                (post.title, post.content, post.published))
                    new_post = cur.fetchone()
                    return {"data": new_post}
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    try:
            with pool.connection() as conn:  
                with conn.cursor(row_factory=psycopg.rows.dict_row) as cur: 
                    cur.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
                    deleted_post = cur.fetchone()
                    
                    if deleted_post is None: 
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post con id {id} no encontrado")
                    
                    return deleted_post
                
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
    


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    try:
        with pool.connection() as conn:  
            with conn.cursor(row_factory=psycopg.rows.dict_row) as cur: 
                cur.execute("UPDATE posts SET title = %s, content= %s, published = %s WHERE id = %s RETURNING *",
                        (post.title, post.content, post.published,id,))
                deleted_post = cur.fetchone()
                
                if deleted_post is None: 
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post con id {id} no encontrado")
                
                return deleted_post
                    
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))





