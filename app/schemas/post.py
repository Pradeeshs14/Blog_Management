from datetime import datetime

from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class PostUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    image: str | None = None

    class Config:
        from_attributes = True

class PaginatedPostResponse(BaseModel):
    posts: list[PostResponse]
    total: int
    page: int
    limit: int
    total_pages: int