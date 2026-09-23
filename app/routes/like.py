from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.like import Like
from app.models.post import Post
from app.models.user import User

from app.schemas.like import LikeResponse

from app.core.security import get_current_user

from app.models.notification import Notification

from app.services.notification_service import send_post_notification

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
    background_tasks: BackgroundTasks,
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


    if post.author_id != current_user.id:
        notification = Notification(
        user_id=post.author_id,
        message=f"{current_user.username} liked your post '{post.title}'",
        notification_type="like",
        is_read=False,
    )

    db.add(notification)
    db.commit()

    post_owner = (
        db.query(User)
        .filter(User.id == post.author_id)
        .first()
    )

    if post_owner and post_owner.email != current_user.email:
        background_tasks.add_task(
            send_post_notification,
            recipient=post_owner.email,
            recipient_name=post_owner.username,
            post_title=post.title,
            actor_name=current_user.username,
            activity="Liked your post",
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