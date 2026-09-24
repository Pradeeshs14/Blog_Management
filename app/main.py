from dotenv import load_dotenv
from fastapi.responses import FileResponse

load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.models import User, Post, Comment, Like, Notification

from app.routes.auth import router as auth_router
from app.routes.post import router as post_router
from app.routes.comment import router as comment_router
from app.routes.like import router as like_router
from app.routes.subscription import router as subscription_router
from app.routes.dashboard import router as dashboard_router
from app.routes.notification import router as notification_router
from app.routes.ai_support import router as ai_support_router

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
app.include_router(subscription_router)
app.include_router(dashboard_router)
app.include_router(notification_router)
app.include_router(ai_support_router)

@app.get("/dashboard")
def dashboard():
    return FileResponse("app/static/dashboard.html")
    
@app.get("/")
def root():
    return {"message": "Blog Management API is running"}