import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel

from app.entities.query_history import QueryHistory
from app.entities.messages import Message
from app.entities.charts import Chart
from app.entities.chart_data import ChartData
from app.entities.products import Product
from app.entities.sales import Sale

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
        
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
        