from pydantic import BaseModel, Field
from app.enums.moods import MoodsEnum
from typing import Optional
from datetime import date,datetime


class MoodSchema(BaseModel):
    id: int
    mood: MoodsEnum
    date: date
    comment: Optional[str] = Field(None)
    created_at: datetime
    updated_at: datetime


class MoodCreateSchema(BaseModel):
    mood: MoodsEnum
    date: date
    comment: Optional[str] = Field(None)


class MoodUpdateSchema(BaseModel):
    mood: MoodsEnum
    comment: Optional[str] = Field(None)
