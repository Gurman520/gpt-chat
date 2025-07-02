from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import ConversationSchema, MessageSchema
from ..dependencies import get_current_user, get_db
import app.applogic.chat as ch


router = APIRouter()

@router.get("/", response_model=list[ConversationSchema])
async def get_conversations(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)):
    return ch.get_conversations(current_user, db)

@router.post("/", response_model=ConversationSchema)
async def create_conversation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ch.create_conversation(current_user, db)

@router.get("/{conversation_id}/messages", response_model=list[MessageSchema])
async def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    return ch.get_messages(conversation_id, db)


@router.post("/{conversation_id}/messages", response_model=MessageSchema)
async def create_message(
    conversation_id: int, 
    request: Request, 
    db: Session = Depends(get_db)):
    data = await request.json()
    user_message = data.get("message")
    return ch.create_message(conversation_id, user_message, db)


@router.patch("/{conversation_id}", response_model=ConversationSchema)
async def update_conversation(
    conversation_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):   
    data = await request.json()
    new_title = data.get("title")
    return ch.update_conversation(conversation_id, new_title, current_user, db)
