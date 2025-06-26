from fastapi import FastAPI
from sqlmodel import Session
from sqlalchemy import text

from app.database.config import engine

app = FastAPI()

@app.on_event("startup")
def startup_event():
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}")

@app.get("/ping")
def home():
    return {"message": "pong"}