import os

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.subscription import Subscription
from app.models.subscription_plan import SubscriptionPlan
from app.models.user import User
from app.models.billing_history import BillingHistory
from app.models.notification import Notification

from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionResponse,
    SubscriptionPlanResponse,
    BillingHistoryResponse,
)

from app.core.security import get_current_user
from app.utils.invoice import generate_invoice
from app.utils.subscription_limits import get_active_subscription


router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"],
)


@router.get("/plans", response_model=list[SubscriptionPlanResponse])
def get_subscription_plans(
    db: Session = Depends(get_db),
):
    return db.query(SubscriptionPlan).order_by(
        SubscriptionPlan.id
    ).all()


@router.post("/", response_model=SubscriptionResponse)
def create_subscription(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plan = db.query(SubscriptionPlan).filter(
        SubscriptionPlan.id == subscription.plan_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found",
        )

    active_subscription = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == current_user.id,
            Subscription.is_active == 1,
        )
        .first()
    )

    if active_subscription:
        raise HTTPException(
            status_code=400,
            detail="You already have an active subscription",
        )

    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=30)

    new_subscription = Subscription(
        user_id=current_user.id,
        plan_id=plan.id,
        start_date=start_date,
        end_date=end_date,
        is_active=1,
    )

    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    notification = Notification(
        user_id=current_user.id,
        message=f"Your {plan.name} subscription has been activated successfully.",
        notification_type="subscription",
        is_read=False,
    )

    db.add(notification)
    db.commit()

    billing_record = BillingHistory(
        user_id=current_user.id,
        plan_id=plan.id,
        plan_name=plan.name,
        price=plan.price,
        start_date=start_date,
        end_date=end_date,
        transaction_id=f"SUB-{new_subscription.id}",
    )

    db.add(billing_record)
    db.commit()
    db.refresh(billing_record)

    invoice_filename = f"invoice_{billing_record.id}.pdf"

    invoice_dir = os.path.join(
        "media",
        "invoices",
    )

    os.makedirs(
        invoice_dir,
        exist_ok=True,
    )

    invoice_path = os.path.join(
        invoice_dir,
        invoice_filename,
    )

    generate_invoice(
        invoice_path=invoice_path,
        transaction_id=billing_record.transaction_id,
        username=current_user.username,
        plan_name=plan.name,
        price=plan.price,
        start_date=start_date,
        end_date=end_date,
    )

    billing_record.invoice_path = invoice_path

    db.commit()
    db.refresh(billing_record)

    return {
        "id": new_subscription.id,
        "user_id": new_subscription.user_id,
        "plan_id": plan.id,
        "plan_name": plan.name,
        "price": plan.price,
        "start_date": new_subscription.start_date,
        "end_date": new_subscription.end_date,
        "is_active": new_subscription.is_active,
    }


@router.post("/renew", response_model=SubscriptionResponse)
def renew_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == current_user.id,
            Subscription.is_active == 1,
        )
        .first()
    )

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="No active subscription found",
        )

    plan = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.id == subscription.plan_id
        )
        .first()
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found",
        )

    old_end_date = subscription.end_date

    new_end_date = old_end_date + timedelta(days=30)

    subscription.end_date = new_end_date

    billing_record = BillingHistory(
        user_id=current_user.id,
        plan_id=plan.id,
        plan_name=plan.name,
        price=plan.price,
        start_date=old_end_date,
        end_date=new_end_date,
        transaction_id=f"RENEW-{subscription.id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
    )

    db.add(billing_record)

    notification = Notification(
        user_id=current_user.id,
        message=f"Your {plan.name} subscription has been renewed successfully.",
        notification_type="subscription",
        is_read=False,
    )

    db.add(notification)

    db.commit()

    db.refresh(subscription)
    db.refresh(billing_record)

    return {
        "id": subscription.id,
        "user_id": subscription.user_id,
        "plan_id": plan.id,
        "plan_name": plan.name,
        "price": plan.price,
        "start_date": subscription.start_date,
        "end_date": subscription.end_date,
        "is_active": subscription.is_active,
    }


@router.get("/me", response_model=SubscriptionResponse)
def get_my_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    subscription, plan = get_active_subscription(
        db,
        current_user.id,
    )

    return {
        "id": subscription.id,
        "user_id": subscription.user_id,
        "plan_id": plan.id,
        "plan_name": plan.name,
        "price": plan.price,
        "start_date": subscription.start_date,
        "end_date": subscription.end_date,
        "is_active": subscription.is_active,
    }


@router.get(
    "/billing-history",
    response_model=list[BillingHistoryResponse],
)
def get_billing_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    billing_history = (
        db.query(BillingHistory)
        .filter(
            BillingHistory.user_id == current_user.id
        )
        .order_by(BillingHistory.id.desc())
        .all()
    )

    return billing_history


@router.get("/billing-history/{billing_id}/invoice")
def download_invoice(
    billing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    billing_record = (
        db.query(BillingHistory)
        .filter(
            BillingHistory.id == billing_id,
            BillingHistory.user_id == current_user.id,
        )
        .first()
    )

    if not billing_record:
        raise HTTPException(
            status_code=404,
            detail="Billing record not found",
        )

    if (
        not billing_record.invoice_path
        or not os.path.exists(billing_record.invoice_path)
    ):
        raise HTTPException(
            status_code=404,
            detail="Invoice file not found",
        )

    return FileResponse(
        path=billing_record.invoice_path,
        media_type="application/pdf",
        filename=f"invoice_{billing_record.id}.pdf",
    )