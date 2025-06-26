from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .sales import Sale

class Product(SQLModel, table=True):
    __tablename__ = "products"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    sales: List[Sale] = Relationship(back_populates="products")