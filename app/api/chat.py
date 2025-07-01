from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..models import Conversation, Message, User
from ..schemas import ConversationSchema, MessageSchema
from ..dependencies import get_db, get_current_user
from ..utils.formatter import format_llama_response
import requests
from datetime import datetime

router = APIRouter()

# URL до Ламы
LLAMA_API_URL = "http://localhost:11434"


@router.get("/conversations", response_model=list[ConversationSchema])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Conversation).filter(Conversation.user_id == current_user.id).all()

@router.post("/conversations", response_model=ConversationSchema)
async def create_conversation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv = Conversation(
        title=f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        user_id=current_user.id
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageSchema])
async def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()
    return messages

@router.post("/conversations/{conversation_id}/messages", response_model=MessageSchema)
async def create_message(conversation_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    user_message = data.get("message")
    
    if not user_message:
        return {"error": "Message is required"}
    
    # Сохраняем сообщение пользователя
    user_msg = Message(
        conversation_id=conversation_id,
        role="user",
        content=user_message
    )
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)
    
    try:
        # Отправляем запрос к Llama
        response = requests.post(
            f"{LLAMA_API_URL}/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": user_message,
                "stream": False
            }
        )
        
        # Обработка ответа
        if response.status_code == 200:
            try:
                result = response.json()
                llama_response = result.get("response", "")
            except ValueError:
                llama_response = "Error parsing Llama response"
        else:
            llama_response = f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        llama_response = f"API Error: {str(e)}"
    
    # Сохраняем ответ модели
    assistant_msg = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=format_llama_response(llama_response)
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)
    
    return assistant_msg