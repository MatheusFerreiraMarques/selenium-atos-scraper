from pydantic import BaseModel
from datetime import date

class UsuarioCreate(BaseModel):
    username: str
    password: str

class AtoCreate(BaseModel):
    name: str
    tipo_ato: str
    numero_ato: int
    orgao: str
    publicacao: date
    ementa: str

class AtoUpdate(BaseModel):
    name: str | None = None
    tipo_ato: str | None = None
    numero_ato: int | None = None
    orgao: str | None = None
    publicacao: date | None = None
    ementa: str | None = None

class AtoResponse(BaseModel):
    id: int
    name: str
    tipo_ato: str
    numero_ato: int
    orgao: str
    publicacao: date
    ementa: str
    class Config:
        from_attributes = True

class RpaLogCreate(BaseModel):
    quantidade_registros: int
    sucessos: int
    erros: int
    tempo_execucao: int

class ScheduleCreate(BaseModel):
    tipo: str
    hora: int | None = None
    minuto: int | None = None
    intervalo_horas: int | None = None
    intervalo_minutos: int | None = None