from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api import auth, chat, base
from .models import init_db


app = FastAPI()

# Инициализация БД
init_db()

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Подключение роутов
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/conversations", tags=["chat"])
app.include_router(base.router, tags=["base"])
