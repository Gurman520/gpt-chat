from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, sessionmaker
from jwt import PyJWTError
from .models import User
from .utils.security import decode_token
from .models import engine


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        if not payload:
            raise credentials_exception
        
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise credentials_exception
        
        return user
    except PyJWTError:
        raise credentials_exception