from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select
from database import obter_sessao
from models import Produto, Utilizador
from auth import obter_utilizador_atual
import io
import csv

router = APIRouter(prefix="/relatorios", tags=["Relatórios e Auditoria"])

@router.get("/produtos/csv")
def exportar_produtos_csv(session: Session = Depends(obter_sessao), utilizador: Utilizador = Depends(obter_utilizador_atual)):
    produtos = session.exec(select(Produto)).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Nome", "Descricao", "Preco", "Em Stock"])
    
    for p in produtos:
        writer.writerow([p.id, p.nome, p.descricao, p.preco, p.em_stock])
        
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment;filename=relatorio_produtos.csv"}
    )