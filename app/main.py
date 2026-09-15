from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.models import User, Post, Comment, Like

from app.routes.auth import router as auth_router
from app.routes.post import router as post_router
from app.routes.comment import router as comment_router
from app.routes.like import router as like_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog Management API",
    description="A mini blogging system built with FastAPI",
    version="1.0.0",
)
app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(like_router)

@app.get("/")
def root():
    return {"message": "Blog Management API is running"}