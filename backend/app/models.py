from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Block(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    title: str
    start_iso: datetime
    end_iso: datetime
    completed: bool = False

