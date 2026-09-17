from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.database import Base


class BillingHistory(Base):
    __tablename__ = "billing_history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)

    plan_name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    transaction_id = Column(String(100), unique=True, nullable=False)
    invoice_path = Column(String(500), nullable=True)