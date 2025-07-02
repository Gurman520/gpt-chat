from fastapi import HTTPException
import app.db.chat as ch
from ..models import Conversation, Message
from datetime import datetime
from ..utils.formatter import format_llama_response
import requests


# URL до ollama 
LLAMA_API_URL = "http://localhost:11434"

def get_conversations(current_user, db):
    return ch.get_conversations(current_user, db)

def create_conversation(current_user, db):
    conv = Conversation(
        title=f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        user_id=current_user.id
    )
    ch.create_conversation(conv, db)
    return conv


def update_conversation(conversation_id, new_title, current_user, db):
       
    if not new_title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    conv = ch.get_conversation(current_user, conversation_id, db)
    
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    ch.update_title(conv, new_title, db)
    return conv


def get_messages(conversation_id, db):
    return ch.get_messages(conversation_id, db)


def create_message(conversation_id, user_message, db):    
    if not user_message:
        return {"error": "Message is required"}
    
    # Сохраняем сообщение пользователя
    user_msg = Message(
        conversation_id=conversation_id,
        role="user",
        content=user_message
    )
    ch.create_message(user_msg, db)
    
    try:
        # Отправляем запрос к Llama
        response = requests.post(
            f"{LLAMA_API_URL}/api/generate",
            json={
                "model": "llama3:8b",
                # "model": "gemma3n",
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
    ch.create_message(assistant_msg, db)
    
    return assistant_msg
