from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user

from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like

from app.schemas.dashboard import DashboardResponse, PostAnalytics


router = APIRouter(
    prefix="/user/dashboard",
    tags=["Dashboard"],
)


@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    posts = (
        db.query(Post)
        .filter(Post.author_id == current_user.id)
        .all()
    )

    total_posts = len(posts)

    total_comments = (
        db.query(Comment)
        .filter(Comment.user_id == current_user.id)
        .count()
    )

    total_likes_received = (
        db.query(Like)
        .join(Post, Like.post_id == Post.id)
        .filter(Post.author_id == current_user.id)
        .count()
    )

    post_analytics = []

    for post in posts:
        likes = (
            db.query(Like)
            .filter(Like.post_id == post.id)
            .count()
        )

        comments = (
            db.query(Comment)
            .filter(Comment.post_id == post.id)
            .count()
        )

        post_analytics.append(
            PostAnalytics(
                post_id=post.id,
                title=post.title,
                likes=likes,
                comments=comments,
            )
        )

    total_views = sum(post.views for post in posts)

    return DashboardResponse(
    total_posts=total_posts,
    total_comments=total_comments,
    total_likes_received=total_likes_received,
    total_views=total_views,
    posts=post_analytics,
)