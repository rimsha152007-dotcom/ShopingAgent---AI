#Yeh user ki message aur session ID ko lekar run_agent_loop ko chalayega

from urllib import response

from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session 
from app.db.session import get_db
from app.schemas.chat import chatRequest,ChatREsponse
from app.agent.loop import run_agent_loop

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("/", response_model=ChatREsponse)
def chat_with_agent(payload: chatRequest, db: Session = Depends(get_db)):
    # Run the agent orchestration loop built in Phase 10
    agent_response = run_agent_loop(
        db=db,
        user_id=payload.user_id,
        session_id=payload.session_id,
        user_message=payload.message
    )

    return ChatREsponse(
        session_id=payload.session_id,
        response=agent_response
    )