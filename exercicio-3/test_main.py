import pytest
from fastapi.testclient import TestClient
from main import app

# FIXTURES (Dados e Client de Teste)

@pytest.fixture
def client():
    return TestClient(app) # Instancia o TestClient usando a nossa aplicação FastAPI

@pytest.fixture
def valid_product():
    return {"name": "Teclado Mecânico", "price": 250.00}

@pytest.fixture
def invalid_product():
    return {"name": "A", "price": -10.0} # Nome muito curto e preço negativo (validação do Pydantic terá falha)

# CENÁRIOS DE TESTE

# 1. Teste criação produto com dados válidos (Cenário Positivo)
def test_create_product_valid(client, valid_product):
    response = client.post("/products/", json=valid_product)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == valid_product["name"]
    assert data["price"] == valid_product["price"]
    assert "id" in data

# 2. Teste validação do POST com dados inválidos (Cenário Negativo)
def test_create_product_invalid(client, invalid_product):
    response = client.post("/products/", json=invalid_product)
    
    # O FastAPI/Pydantic retorna 422 para erros de validação
    assert response.status_code == 422
    assert "detail" in response.json()

# 3. Teste GET com ID existente (Cenário Positivo)
def test_get_product_existing(client, valid_product):
    # Setup: Primeiro criamos o produto para garantir que o ID existe
    create_response = client.post("/products/", json=valid_product)
    product_id = create_response.json()["id"]
    
    response = client.get(f"/products/{product_id}")
    
    assert response.status_code == 200
    assert response.json()["id"] == product_id
    assert response.json()["name"] == valid_product["name"]

# 4. Teste GET com ID inexistente (Cenário Negativo)
def test_get_product_non_existing(client):
    response = client.get("/products/9999")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Produto não encontrado"}