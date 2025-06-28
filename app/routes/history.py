from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import select, Session, desc

from app.database.config import get_session
from app.entities.query_history import QueryHistory, QueryHistoryRead

router = APIRouter()

@router.get("/", response_model=list[QueryHistory])
def get_query_history(session: Session = Depends(get_session)):
    """
    Retrieve the entire query history.
    """
    statement = select(QueryHistory).order_by(desc(QueryHistory.created_at))
    history = session.exec(statement).all()
    return history

@router.get("/{history_id}", response_model=QueryHistoryRead)
def get_query_history_by_id(history_id: int, session: Session = Depends(get_session)):
    statement = (
        select(QueryHistory)
        .where(QueryHistory.id == history_id)
        .options(selectinload(QueryHistory.messages))
    )
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="Query history not found")

    print(f"Mensajes en history_id {history_id}: {len(result.messages)}")
    return result

@router.delete("/{history_id}", response_model=QueryHistory)
def delete_query_history(history_id: int, session: Session = Depends(get_session)):
    """
    Delete a specific query history entry by its ID.
    """
    history = session.get(QueryHistory, history_id)
    if not history:
        raise HTTPException(status_code=404, detail="Query history not found")

    session.delete(history)
    session.commit()
    return history
