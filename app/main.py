from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import requests
from datetime import datetime
from .models import get_db, init_db, Conversation, Message
from .schemas import MessageSchema, ConversationSchema
from .format import format_llama_response

app = FastAPI()

# Инициализация БД
init_db()

# Настройка статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# URL до Ламы
LLAMA_API_URL = "http://localhost:11434"


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")


@app.get("/")
async def chat_interface(request: Request, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).all()
    return templates.TemplateResponse("base.html", {
        "request": request,
        "conversations": [conv.to_dict() for conv in conversations]
    })

@app.post("/api/conversations", response_model=ConversationSchema)
async def create_conversation(db: Session = Depends(get_db)):
    conv = Conversation(title=f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

@app.get("/api/conversations/{conversation_id}/messages", response_model=list[MessageSchema])
async def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()
    return messages

@app.post("/api/conversations/{conversation_id}/messages", response_model=MessageSchema)
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