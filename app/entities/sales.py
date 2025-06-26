from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.entities.products import Product
    
class Sale(SQLModel, table=True):
    __tablename__ = "sales"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    ticket_number: str
    date: datetime = Field(default_factory=datetime.utcnow)
    week_day: str
    hour: str
    quantity: int
    unitary_price: float
    total: float
    
    product: Optional["Product"] = Relationship(back_populates="sales")