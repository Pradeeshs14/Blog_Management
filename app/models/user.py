from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    email = Column(
    String(100),
    unique=True,
    nullable=True,
    index=True,
)

    password = Column(
        String(255),
        nullable=False,
    )

    name = Column(
        String(100),
        nullable=True,
    )

    provider = Column(
        String(50),
        nullable=True,
    )

    auth0_id = Column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
    )

    subscriptions = relationship(
        "Subscription",
        backref="user",
    )