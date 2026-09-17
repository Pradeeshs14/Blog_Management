from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.like import Like
from app.models.post import Post
from app.models.user import User

from app.schemas.like import LikeResponse

from app.core.security import get_current_user
from app.core.email import send_email

from app.utils.subscription_limits import (
    get_active_subscription,
    check_limit,
)


router = APIRouter(
    prefix="/posts/{post_id}/like",
    tags=["Likes"],
)


@router.post("/", response_model=LikeResponse)
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    existing_like = (
        db.query(Like)
        .filter(
            Like.post_id == post_id,
            Like.user_id == current_user.id,
        )
        .first()
    )

    if existing_like:
        raise HTTPException(
            status_code=400,
            detail="You already liked this post",
        )

    subscription, plan = get_active_subscription(
        db,
        current_user.id,
    )

    like_count = (
        db.query(Like)
        .filter(Like.user_id == current_user.id)
        .count()
    )

    check_limit(
        db,
        current_user.id,
        like_count,
        plan.max_likes,
    )

    like = Like(
        post_id=post_id,
        user_id=current_user.id,
    )

    db.add(like)
    db.commit()
    db.refresh(like)

    post_owner = (
        db.query(User)
        .filter(User.id == post.author_id)
        .first()
    )

    if post_owner and post_owner.email != current_user.email:
        send_email(
            recipient=post_owner.email,
            subject="New Like on Your Blog Post",
            body=(
                f"Hello {post_owner.username},\n\n"
                f"{current_user.username} liked your post "
                f'"{post.title}".\n'
            ),
        )

    return like


@router.delete("/")
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    like = (
        db.query(Like)
        .filter(
            Like.post_id == post_id,
            Like.user_id == current_user.id,
        )
        .first()
    )

    if not like:
        raise HTTPException(
            status_code=404,
            detail="You have not liked this post",
        )

    db.delete(like)
    db.commit()

    return {
        "message": "Post unliked successfully"
    }