from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from .api import auth, chat
from .models import init_db

app = FastAPI()

# Инициализация БД
init_db()

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Подключение роутов
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")
