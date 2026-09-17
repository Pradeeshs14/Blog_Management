from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class PostImage(Base):
    __tablename__ = "post_images"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    image_path = Column(String(500), nullable=False)