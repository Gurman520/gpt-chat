from fastapi import HTTPException, status
from ..utils.security import (
    get_password_hash,
    verify_password,
    create_access_token
)
from ..models import User
import app.db.login as lg


def register(user, db):
    db_user = lg.get_user(user, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    lg.create_user(db_user, db)
    return {"message": "User created successfully"}

def login(form_data, db):
    user = lg.get_user(form_data, db)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

