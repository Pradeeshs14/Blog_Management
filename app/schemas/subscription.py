from datetime import datetime
from pydantic import BaseModel


class SubscriptionCreate(BaseModel):
    plan_id: int


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan_id: int
    plan_name: str
    price: float
    start_date: datetime
    end_date: datetime
    is_active: int

    class Config:
        from_attributes = True

class SubscriptionPlanResponse(BaseModel):
    id: int
    name: str
    price: float
    max_posts: int | None
    max_images_per_post: int | None
    max_likes: int | None
    max_comments: int | None

    class Config:
        from_attributes = True

class BillingHistoryResponse(BaseModel):
    id: int
    user_id: int
    plan_id: int
    plan_name: str
    price: float
    start_date: datetime
    end_date: datetime
    transaction_id: str
    invoice_path: str | None

    class Config:
        from_attributes = True