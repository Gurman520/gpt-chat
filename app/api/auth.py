from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import Token, UserCreate
from ..dependencies import get_db, get_current_user
import app.applogic.login as lg
from app.logger import logger


router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("Вызван API Регистрации")
    return lg.register(user, db)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info("Вызван API Входа")
    return lg.login(form_data, db)

@router.get("/verify")
async def verify_token(current_user: User = Depends(get_current_user)):
    logger.info("Вызван API Верификации")
    return current_user
