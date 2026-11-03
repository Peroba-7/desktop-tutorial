from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from database import criar_tabelas, obter_sessao
from models import Utilizador
from routers import produtos, movimentos, relatorios
from auth import criar_token_acesso, obter_password_hash, verificar_password

app = FastAPI(
    title="DOMO API Comercial - Enterprise Edition",
    description="""
    ## Sistema Oficial de Gestão Comercial - DOMO
    
    * **Desenvolvimento e Backend**: Arquitetura Modular em FastAPI & SQLModel
    * **Direção Técnica**: Responsável Técnico
    * **Gestão Comercial**: Gestão Comercial
    """,
    version="3.0.0",
)

app.include_router(produtos.router)
app.include_router(movimentos.router)
app.include_router(relatorios.router)

@app.post("/token", tags=["Autenticação"])
def login_para_obter_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(obter_sessao)):
    statement = select(Utilizador).where(Utilizador.username == form_data.username)
    utilizador = session.exec(statement).first()
    
    # Se for o primeiro arranque e não existir utilizador, criamos o admin padrão
    if not utilizador and form_data.username == "admin" and form_data.password == "domo123":
        novo_admin = Utilizador(username="admin", hashed_password=obter_password_hash("domo123"), role="admin")
        session.add(novo_admin)
        session.commit()
        utilizador = novo_admin

    if not utilizador or not verificar_password(form_data.password, utilizador.hashed_password):
        raise HTTPException(status_code=400, detail="Utilizador ou palavra-passe incorretos.")
    
    access_token = criar_token_acesso(data={"sub": utilizador.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/", tags=["Início"])
def raiz():
    return {
        "sistema": "DOMO API Comercial",
        "estado": "Operacional - Enterprise",
        "versao": "3.0.0"
    }