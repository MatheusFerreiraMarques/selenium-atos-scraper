from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Atos
from database import get_db
from auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/dashboard", tags=["Logs"])

@router.get("/")
def dashboard(
    data_inicio: str | None = None,
    data_fim: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(Atos).filter(Atos.ativo==True)
    if data_inicio and data_fim:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d").date()
        query = query.filter(Atos.publicacao>=data_inicio_dt, Atos.publicacao<=data_fim_dt)
    total_atos = query.count()
    por_orgao = query.with_entities(Atos.orgao, func.count(Atos.id)).group_by(Atos.orgao).all()
    por_tipo = query.with_entities(Atos.tipo_ato, func.count(Atos.id)).group_by(Atos.tipo_ato).all()
    return {
        "total_atos": total_atos,
        "atos_por_orgao": [{"orgao": o, "quantidade": q} for o, q in por_orgao],
        "atos_por_tipo": [{"tipo_ato": t, "quantidade": q} for t, q in por_tipo]
    }