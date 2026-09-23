from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.notification import Notification
from app.schemas.notification import (
    NotificationResponse,
    NotificationUnreadCount,
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


# ==========================================
# GET ALL NOTIFICATIONS
# ==========================================
@router.get("/", response_model=list[NotificationResponse])
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return notifications


# ==========================================
# GET UNREAD NOTIFICATION COUNT
# ==========================================
@router.get(
    "/unread-count",
    response_model=NotificationUnreadCount,
)
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    unread_count = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False,
        )
        .count()
    )

    return {
        "unread_count": unread_count
    }


# ==========================================
# MARK ALL NOTIFICATIONS AS READ
# ==========================================
@router.put("/read-all")
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False,
        )
        .all()
    )

    for notification in notifications:
        notification.is_read = True

    db.commit()

    return {
        "message": "All notifications marked as read"
    }


# ==========================================
# MARK SINGLE NOTIFICATION AS READ
# ==========================================
@router.put(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification


# ==========================================
# MARK SINGLE NOTIFICATION AS UNREAD
# ==========================================
@router.put(
    "/{notification_id}/unread",
    response_model=NotificationResponse,
)
def mark_as_unread(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    notification.is_read = False

    db.commit()
    db.refresh(notification)

    return notification