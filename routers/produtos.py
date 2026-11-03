from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import obter_sessao
from models import Produto
from auth import obter_utilizador_atual
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DOMO-API")

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/", response_model=list[Produto])
def listar_produtos(
    skip: int = Query(0, description="Número de registos a saltar (paginação)"),
    limit: int = Query(10, description="Número máximo de registos a devolver"),
    nome: str | None = Query(None, description="Filtrar por parte do nome do produto"),
    session: Session = Depends(obter_sessao)
):
    statement = select(Produto)
    if nome:
        statement = statement.where(Produto.nome.contains(nome))
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all()

@router.post("/", response_model=Produto, status_code=201)
def criar_produto(
    produto: Produto, 
    session: Session = Depends(obter_sessao), 
    utilizador: str = Depends(obter_utilizador_atual)
):
    session.add(produto)
    session.commit()
    session.refresh(produto)
    logger.info(f"[AUDITORIA] Utilizador '{utilizador}' criou o produto: ID {produto.id} - {produto.nome}")
    return produto

@router.get("/{produto_id}", response_model=Produto)
def obter_produto(produto_id: int, session: Session = Depends(obter_sessao)):
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado no sistema DOMO.")
    return produto

@router.put("/{produto_id}", response_model=Produto)
def atualizar_produto(
    produto_id: int, 
    produto_atualizado: Produto, 
    session: Session = Depends(obter_sessao),
    utilizador: str = Depends(obter_utilizador_atual)
):
    produto_db = session.get(Produto, produto_id)
    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado no sistema DOMO.")
    
    produto_dados = produto_atualizado.model_dump(exclude_unset=True)
    for chave, valor in produto_dados.items():
        setattr(produto_db, chave, valor)
        
    session.add(produto_db)
    session.commit()
    session.refresh(produto_db)
    logger.info(f"[AUDITORIA] Utilizador '{utilizador}' atualizou o produto ID {produto_id}")
    return produto_db

@router.delete("/{produto_id}")
def apagar_produto(
    produto_id: int, 
    session: Session = Depends(obter_sessao),
    utilizador: str = Depends(obter_utilizador_atual)
):
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado no sistema DOMO.")
    
    session.delete(produto)
    session.commit()
    logger.warning(f"[AUDITORIA] Utilizador '{utilizador}' eliminou o produto ID {produto_id}")
    return {"mensagem": f"Produto com o ID {produto_id} foi eliminado com sucesso do sistema DOMO."}