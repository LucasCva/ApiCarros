from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from models.carro_model import Carros
from shared.dependencies import get_db

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:802175@172.17.0.3/db_carros_test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


# Cria uma sessão local para o comunicação com o banco
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def testar_carros():

    with TestingSessionLocal() as test_db:
        test_carro = Carros(nome="CarroT", ano=2022, modelo="ModeloT")
        test_db.add(test_carro)
        test_db.commit()

    response = client.get('/carros')
    # espero que o status code
    assert response.status_code == 200
    carro_response = response.json()
    assert carro_response[0]["nome"] == "CarroT"

def testar_criar_carros():
    carro_novo = {"nome": "CarroT", "ano": 2022, "modelo": "ModeloT"}
    response = client.post("/carros", json=carro_novo)
    assert response.status_code == 202
