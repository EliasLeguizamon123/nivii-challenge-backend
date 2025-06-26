from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from .chart_data import ChartData, ChartDataRead

if TYPE_CHECKING:
    from app.entities.query_history import QueryHistory
    
class ChartRead(SQLModel):
    id: int
    history_id: int
    chart_type: str
    title: str
    x_axis: str     
    y_axis: str      
    created_at: datetime
    data: List[ChartDataRead] = []
    
    class Config:
        orm_mode = True
    
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
    data: List["ChartData"] = Relationship(back_populates="chart")