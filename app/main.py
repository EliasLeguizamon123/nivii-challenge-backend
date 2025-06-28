import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.config import engine, create_db_and_tables
from app.routes import ping, messages, history

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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