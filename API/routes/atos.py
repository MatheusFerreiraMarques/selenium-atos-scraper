from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models import Atos
from schemas import AtoCreate, AtoUpdate, AtoResponse
from auth import get_current_user   
from database import get_db

router = APIRouter(prefix="/atos", tags=["Atos"])

@router.post("/", response_model=AtoResponse)
def create_ato(
    ato: AtoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        db_ato = Atos(**ato.model_dump())
        db.add(db_ato)
        db.commit()
        db.refresh(db_ato)
        return db_ato

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Ato já cadastrado"
        )
    except:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.get("/{ato_id}", response_model=AtoResponse)
def get_ato(ato_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    ato = db.query(Atos).filter(Atos.id == ato_id, Atos.ativo==True).first()
    if not ato:
        raise HTTPException(status_code=404, detail="Ato não encontrado")
    return ato

@router.get("/", response_model=list[AtoResponse])
def list_atos(
    data_inicio: str | None = None,
    data_fim: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(Atos).filter(Atos.ativo==True)
    if data_inicio:
        query = query.filter(Atos.publicacao >= data_inicio)
    if data_fim:
        query = query.filter(Atos.publicacao <= data_fim)
    if search:
        query = query.filter(
            (Atos.tipo_ato.ilike(f"%{search}%")) |
            (Atos.orgao.ilike(f"%{search}%")) |
            (Atos.ementa.ilike(f"%{search}%"))
        )
    return query.all()

@router.put("/{ato_id}", response_model=AtoResponse)
def update_ato(ato_id: int, ato_update: AtoUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    ato = db.query(Atos).filter(Atos.id == ato_id, Atos.ativo==True).first()
    if not ato:
        raise HTTPException(status_code=404, detail="Ato não encontrado")
    for key, value in ato_update.model_dump(exclude_unset=True).items():
        setattr(ato, key, value)
    db.commit()
    db.refresh(ato)
    return ato

@router.delete("/{ato_id}")
def delete_ato(
    ato_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    ato = db.query(Atos).filter(
        Atos.id == ato_id,
        Atos.ativo == True
    ).first()

    if not ato:
        raise HTTPException(status_code=404, detail="Ato não encontrado")

    ato.ativo = False
    db.commit()

    return {"message": "Ato removido com sucesso (delete lógico)"}