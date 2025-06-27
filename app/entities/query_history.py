from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from .messages import Message, MessageRead
from .charts import Chart, ChartRead

class QueryHistoryRead(SQLModel):
    id: int
    title: str
    created_at: datetime
    preview: Optional[str] = None
    messages: List[MessageRead] = []
    charts: List[ChartRead] = []

    class Config:
        orm_mode = True
class QueryHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    preview: Optional[str] = None

    messages: List["Message"] = Relationship(back_populates="history", cascade_delete="all, delete-orphan")
    charts: List["Chart"] = Relationship(back_populates="history", cascade_delete="all, delete-orphan")