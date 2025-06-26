from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.entities.charts import Chart
    
class ChartDataRead(SQLModel):
    id: int
    chart_id: int
    label: str
    value: float        

    class Config:
        orm_mode = True
class ChartData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chart_id: int = Field(foreign_key="charts.id")
    label: str          # Product A
    value: float         # could be quantity, money, etc.

    chart: Optional["Chart"] = Relationship(back_populates="data")