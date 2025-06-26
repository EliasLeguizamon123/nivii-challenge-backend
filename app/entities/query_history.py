from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from .messages import Message
from .charts import Chart

class QueryHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    preview: Optional[str] = None

    messages: List[Message] = Relationship(back_populates="history")
    charts: List[Chart] = Relationship(back_populates="history")