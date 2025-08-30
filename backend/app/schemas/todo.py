# backend/app/schemas/todo.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# Tag Schemas
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True

# Todo Schemas
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None

class TodoCreate(TodoBase):
    tags: List[int] = [] # 传入tag的id列表

class TodoUpdate(TodoBase):
    is_completed: Optional[bool] = None
    tags: Optional[List[int]] = None

class Todo(TodoBase):
    id: int
    is_completed: bool
    owner_id: int
    tags: List[Tag] = []

    class Config:
        from_attributes = True