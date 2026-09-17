
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.models.subscription_plan import SubscriptionPlan


LIMIT_MESSAGE = (
    "You've reached your plan limit. "
    "Kindly upgrade your plan to continue."
)


def get_active_subscription(db: Session, user_id: int):
    # Mark expired subscriptions as inactive
    expired_subscriptions = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == user_id,
            Subscription.is_active == 1,
            Subscription.end_date <= datetime.utcnow(),
        )
        .all()
    )

    for subscription in expired_subscriptions:
        subscription.is_active = 0

    if expired_subscriptions:
        db.commit()

    # Get the latest active subscription
    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == user_id,
            Subscription.is_active == 1,
            Subscription.end_date > datetime.utcnow(),
        )
        .order_by(Subscription.id.desc())
        .first()
    )

    if not subscription:
        raise HTTPException(
            status_code=403,
            detail="No active subscription. Kindly subscribe to a plan to continue.",
        )

    plan = (
        db.query(SubscriptionPlan)
        .filter(SubscriptionPlan.id == subscription.plan_id)
        .first()
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found.",
        )

    return subscription, plan


def check_limit(
    db: Session,
    user_id: int,
    current_count: int,
    limit: int | None,
):
    if limit is not None and current_count >= limit:
        raise HTTPException(
            status_code=403,
            detail=LIMIT_MESSAGE,
        )

