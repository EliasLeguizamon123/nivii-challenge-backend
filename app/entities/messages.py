# app/models/message.py

from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

if TYPE_CHECKING:
    from app.entities.query_history import QueryHistory

class MessageRead(SQLModel):
    id: int
    history_id: int
    type: str
    content: str
    created_at: datetime
    has_chart: Optional[bool] = False

    class Config:
        orm_mode = True
class MessageType(str, Enum):
    user = "user"
    assistant = "assistant"
class Message(SQLModel, table=True):
    __tablename__ = "messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    history_id: int = Field(foreign_key="queryhistory.id")
    type: MessageType
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    has_chart: Optional[bool] = False

    history: Optional["QueryHistory"] = Relationship(back_populates="messages")