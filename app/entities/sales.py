from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field
    
class Sale(SQLModel, table=True):
    __tablename__ = "sales"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    # product_id: int = Field(foreign_key="products.id")
    product_name: str
    waiter: str
    ticket_number: str
    date: datetime = Field(default_factory=datetime.utcnow)
    week_day: str
    hour: str
    quantity: int
    unitary_price: float
    total: float
    
    # product: Optional["Product"] = Relationship(back_populates="sales")