from datetime import datetime

from pydantic import BaseModel


class LikeResponse(BaseModel):
    id: int
    post_id: int
    user_id: int

    class Config:
        from_attributes = True