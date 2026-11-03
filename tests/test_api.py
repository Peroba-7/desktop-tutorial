from fastapi.testclient import TestClient
from main import app
from database import criar_tabelas

# Garante que a base de dados e as tabelas são criadas antes dos testes
criar_tabelas()

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["sistema"] == "DOMO API Comercial"

def test_login_and_create_product():
    # Obter token de acesso
    response = client.post("/token", data={"username": "admin", "password": "domo123"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Criar produto autenticado
    headers = {"Authorization": f"Bearer {token}"}
    produto_data = {
        "nome": "Cabo de Rede Cat6",
        "descricao": "Cabo blindado para infraestruturas",
        "preco": 45.50,
        "em_stock": 100
    }
    response_prod = client.post("/produtos/", json=produto_data, headers=headers)
    assert response_prod.status_code == 201
    assert response_prod.json()["nome"] == "Cabo de Rede Cat6"