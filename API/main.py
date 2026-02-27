from dotenv import load_dotenv
from fastapi import FastAPI
from database import Base, engine
from routes import auth, atos, dashboard, user

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Atos da Receita")
@app.get("/")
def root():
    return {"message": "API rodando!"}

app.include_router(auth.router)
app.include_router(atos.router)
app.include_router(dashboard.router)
app.include_router(user.router)