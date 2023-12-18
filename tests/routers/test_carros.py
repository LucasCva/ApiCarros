from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def testar_carros():
    response = client.get('/carros')
    # espero que o status code
    assert response.status_code == 200
    assert response.json() == [{
        'ano': 2022,
        'id': 1,
        'modelo': 'Fiat',
        'nome': 'Camaro'
    }]


def test_criar_carro():
    novocarro = {
        "nome": "cavalo",
        "ano": 2000,
        "modelo": "carro"
    }
    response = client.post('/carros', json= novocarro)
    assert response.status_code == 202
