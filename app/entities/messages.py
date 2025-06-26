# app/models/message.py

from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.entities.query_history import QueryHistory

class Message(SQLModel, table=True):
    __tablename__ = "messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    history_id: int = Field(foreign_key="queryhistory.id")
    type: str  # 'user' o 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    has_chart: Optional[bool] = False

    history: Optional["QueryHistory"] = Relationship(back_populates="messages")
