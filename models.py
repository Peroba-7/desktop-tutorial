from sqlmodel import SQLModel, Field
from datetime import datetime

class Utilizador(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    role: str = Field(default="operador") # "admin" ou "operador"
    ativo: bool = Field(default=True)

class Produto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    descricao: str
    preco: float
    em_stock: int = Field(default=0)

class MovimentoStock(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    produto_id: int = Field(foreign_key="produto.id")
    tipo: str # "ENTRADA" ou "SAIDA"
    quantidade: int
    utilizador: str
    data: datetime = Field(default_factory=datetime.utcnow)