from fastapi import FastAPI
from sqlmodel import Session
from sqlalchemy import text

from app.database.config import engine, create_db_and_tables
from app.routes import ping, messages, history

app = FastAPI()

app.include_router(ping.router, prefix="/ping")
app.include_router(messages.router, prefix="/messages")
app.include_router(history.router, prefix="/history")

@app.on_event("startup")
def startup_event():
    try:
        create_db_and_tables()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Database connection failed: {e}")