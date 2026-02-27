from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import Usuario
from database import get_db
from auth import criar_token, verificar_senha

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username==form_data.username).first()
    if not user or not verificar_senha(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    access_token = criar_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}