from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User

from app.schemas.comment import CommentCreate, CommentResponse

from app.core.security import get_current_user

from app.models.notification import Notification

from app.services.notification_service import send_post_notification

from app.utils.subscription_limits import (
    get_active_subscription,
    check_limit,
)


router = APIRouter(
    prefix="/posts/{post_id}/comments",
    tags=["Comments"],
)


@router.post("/", response_model=CommentResponse)
def create_comment(
    post_id: int,
    data: CommentCreate,
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

    subscription, plan = get_active_subscription(
        db,
        current_user.id,
    )

    comment_count = (
        db.query(Comment)
        .filter(Comment.user_id == current_user.id)
        .count()
    )

    check_limit(
        db,
        current_user.id,
        comment_count,
        plan.max_comments,
    )

    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        text=data.text,
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    if post.author_id != current_user.id:
        notification = Notification(
        user_id=post.author_id,
        message=f"{current_user.username} commented on your post '{post.title}'",
        notification_type="comment",
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
            activity="Commented on your post",
        )

    return comment


@router.get("/", response_model=list[CommentResponse])
def get_comments(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
        .all()
    )