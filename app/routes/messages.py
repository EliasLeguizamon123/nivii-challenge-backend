from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.database.config import get_session
from app.services.openai import generate_sql_from_natural_language
from app.entities.messages import Message
from app.entities.query_history import QueryHistory, QueryHistoryRead
from app.services.generate_assitant_content_and_chart_data import generate_assistant_content_and_chart_data

router = APIRouter()

@router.post("/", response_model=QueryHistoryRead)
def create_message_with_history(message: Message, session: Session = Depends(get_session)):
    """
    Create a message, if there is no existing query history, create a new one, then send message to OpenAI to generate a SQLite query
    After this send this query into the database and get the data obtained and generate an "assistant" message, insert it into a history.id
    And finally return that entire historyQuery.
    """
    if message.history_id:
        history = session.get(QueryHistory, message.history_id)
        if not history:
            raise HTTPException(status_code=404, detail="Query history not found")
    else:
        history = QueryHistory(
            title=f"{message.content[:20]}...",
            preview=message.content,
            created_at=message.created_at,
        )
        session.add(history)
        session.commit()
        session.refresh(history)

    # Save user message into history
    user_msg = Message(
        content=message.content,
        type=message.type,
        history_id=history.id,
    )
    session.add(user_msg)
    session.commit()
    session.refresh(user_msg)

    # Generate SQLite query
    query = generate_sql_from_natural_language(message.content)
    
    
    print(f"SQLite query: {query}")

    assistant_content = generate_assistant_content_and_chart_data(
        query=query,
        session=session,
        history=history,
        message=user_msg,
    )

    assistant_msg = Message(
        content=assistant_content,
        type="assistant",
        history_id=history.id,
    )
    session.add(assistant_msg)
    session.commit()

    history = session.exec(
        select(QueryHistory)
        .where(QueryHistory.id == history.id)
        .options(
            selectinload(QueryHistory.messages),
            selectinload(QueryHistory.charts),
        )
    ).one()

    return history