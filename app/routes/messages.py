from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.database.config import get_session
from app.services.openai import generate_sql_from_natural_language
from app.entities.messages import Message
from app.entities.query_history import QueryHistory, QueryHistoryRead
from app.services.generate_assitant_content_and_chart_data import generate_assistant_content_and_chart_data
router = APIRouter()

@router.post("/", response_model=QueryHistoryRead)
def create_message_with_history(message: Message, session: Session = Depends(get_session)):
    """
    Create a message, if there is no existing query history, create a new one, then send message to OpenAi to generate a Sqlite query
    After this send this query into database and get the data obtained.
    """
    if message.history_id:
        history = session.get(QueryHistory, message.history_id)
        if not history:
            raise HTTPException(status_code=404, detail="Query history not found")
    else:
        history = QueryHistory(title=f"{message.content[:20]}...", preview=message.content, created_at=message.created_at)
        
        session.add(history)
        session.commit()
        session.refresh(history)
        
    # Save user message into history
    message = Message(
        content=message.content,
        type=message.type,
        history_id=history.id,
    )
    
    session.add(message)
    session.commit()
    session.refresh(message)
    
    # Generate SQLite query
    query = generate_sql_from_natural_language(message.content)
    
    # execute query
    print(f"SQLite query: {query}")
    
    assistant_content, has_chart = generate_assistant_content_and_chart_data(
        query=query,
        session=session,
        history=history,
        message=message
    )
    
    assistant_msg = Message(
        content=assistant_content,
        type="assistant",
        history_id=history.id,
        has_chart=has_chart
    )
    
    session.add(assistant_msg)
    session.commit()
    session.refresh(assistant_msg)
    
    session.refresh(history)

    return history

@router.get("/{history_id}", response_model=List[Message])
def get_messages(history_id: int, session: Session = Depends(get_session)):
    """
    Retrieve all messages for a specific query history entry.
    """
    history = session.get(QueryHistory, history_id)
    if not history:
        raise HTTPException(status_code=404, detail="Query history not found")

    # Order messages by creation time
    statement = select(Message).where(Message.history_id == history_id).order_by(Message.created_at)
    messages = session.exec(statement).all()
    return messages