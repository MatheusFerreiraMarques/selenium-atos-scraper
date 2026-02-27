from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Usuario
from schemas import UsuarioCreate
from database import get_db
from auth import gerar_hash

router = APIRouter(prefix="/user",tags=["Usuário"])

@router.post("/")
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    hashed_password = gerar_hash(user.password)
    novo_usuario = Usuario(username=user.username, password=hashed_password)
    db.add(novo_usuario)
    db.commit()
    return {"message": "Usuário criado com sucesso"}
