# DOMO API - Sistema de Gestão

Aplicação modular desenvolvida em FastAPI com SQLModel e SQLite para gestão de produtos e operações da empresa.

## Estrutura do Projeto
- `main.py`: Ponto de entrada da aplicação e inclusão das rotas.
- `database.py`: Configuração do banco de dados SQLite e sessão.
- `models.py`: Modelos de dados (SQLModel/Pydantic).
- `routers/`: Módulos com os endpoints da API (ex: `produtos.py`).

## Como Executar
1. Ativar o ambiente virtual (`venv`).
2. Instalar as dependências: `pip install sqlmodel fastapi uvicorn`
3. Iniciar o servidor: `uvicorn main:app --reload`
4. Aceder à documentação interativa: `http://127.0.0.1:8000/docs`