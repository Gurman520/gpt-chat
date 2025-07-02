from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import Token, UserCreate
from ..dependencies import get_db, get_current_user
import app.applogic.login as lg

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return lg.register(user, db)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return lg.login(form_data, db)

@router.get("/verify")
async def verify_token(current_user: User = Depends(get_current_user)):
    return current_user
