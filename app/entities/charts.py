from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.entities.query_history import QueryHistory
    
class Chart(SQLModel, table=True):
    __tablename__ = "charts"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    history_id: int = Field(foreign_key="queryhistory.id")
    chart_type: str  # 'bar', 'line', 'pie', etc.
    title: str
    x_axis: str      # product
    y_axis: str      # quantity
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    history: Optional["QueryHistory"] = Relationship(back_populates="charts")