from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import obter_sessao
from models import Produto, MovimentoStock
from models import Utilizador
from auth import obter_utilizador_atual
import logging

logger = logging.getLogger("DOMO-API")
router = APIRouter(prefix="/movimentos", tags=["Movimentos de Stock"])

@router.post("/", response_model=MovimentoStock, status_code=201)
def registar_movimento(
    produto_id: int,
    tipo: str,
    quantidade: int,
    session: Session = Depends(obter_sessao),
    utilizador: Utilizador = Depends(obter_utilizador_atual)
):
    if tipo not in ["ENTRADA", "SAIDA"]:
        raise HTTPException(status_code=400, detail="Tipo de movimento inválido. Use 'ENTRADA' ou 'SAIDA'.")
    
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    
    if tipo == "SAIDA":
        if produto.em_stock < quantidade:
            raise HTTPException(status_code=400, detail="Stock insuficiente para esta saída.")
        produto.em_stock -= quantidade
    else:
        produto.em_stock += quantidade
        
    movimento = MovimentoStock(
        produto_id=produto_id,
        tipo=tipo,
        quantidade=quantidade,
        utilizador=utilizador.username
    )
    
    session.add(movimento)
    session.add(produto)
    session.commit()
    session.refresh(movimento)
    
    logger.info(f"[STOCK] {utilizador.username} registrou {tipo} de {quantidade} unidades no produto ID {produto_id}")
    return movimento

@router.get("/", response_model=list[MovimentoStock])
def listar_movimentos(session: Session = Depends(obter_sessao), utilizador: Utilizador = Depends(obter_utilizador_atual)):
    return session.exec(select(MovimentoStock)).all()