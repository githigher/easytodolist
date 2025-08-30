# backend/app/routers/auth.py

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, security
# --- MODIFIED IMPORTS ---
from app.schemas import user as user_schemas
# --- END MODIFIED IMPORTS ---
from app.db.database import get_db
from app.core.config import settings

router = APIRouter()

@router.post("/token", response_model=user_schemas.Token) # <-- MODIFIED HERE
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED) # <-- MODIFIED HERE
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)): # <-- MODIFIED HERE
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)