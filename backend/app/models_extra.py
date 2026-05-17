from sqlmodel import SQLModel
from typing import Optional

class Health(SQLModel):
    status: str
