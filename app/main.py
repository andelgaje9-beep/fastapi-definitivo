from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .router import Oauth2, authjwtBearer, posts, users, vote
from . import alchemy_models
from .database import engine

app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authjwtBearer.router)
app.include_router(Oauth2.router)
app.include_router(vote.router)


alchemy_models.Base.metadata.create_all(bind=engine)
    
    
@app.get("/")
async def root():
    return {"message": "Hello World"}








