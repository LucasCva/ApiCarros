from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database.models.carro_model import Carros
from shared.database import Base
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


# Recria as tabelas
def database_inicialize():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# Cria carros no banco para teste
def criar_carro_para_test():
    with TestingSessionLocal() as test_db:
        test_carro = Carros(nome="CarroT", ano=2022, modelo="ModeloT")
        test_db.add(test_carro)
        test_db.commit()


app.dependency_overrides[get_db] = override_get_db


# Teste de listar carros
def test_carros():
    criar_carro_para_test()

    response = client.get('/carros')
    # espero que o status code
    assert response.status_code == 200
    carro_response = response.json()
    assert carro_response[0]["nome"] == "CarroT"


# Teste que de criar carros
def test_criar_carros():
    database_inicialize()

    carro_novo = {"nome": "CarroT", "ano": 2022, "modelo": "ModeloT"}
    response = client.post("/carros", json=carro_novo)
    assert response.status_code == 201


# Teste de buscar carro pelo ID
def test_pegar_carro_pelo_ID():
    database_inicialize()

    criar_carro_para_test()

    id_carro = 1
    response = client.get(f"/carros/{id_carro}/")
    assert response.status_code == 200


# Teste de mudar algo pelo ID
def test_update_carro():
    database_inicialize()

    criar_carro_para_test()

    id_carro = 1
    update_carro = {"nome": "CarroT2", "ano": 2023, "modelo": "ModeloT2"}
    response = client.put(f"/carros/{id_carro}/", json=update_carro)
    assert response.status_code == 200


# Teste de deletar carro
def test_delete_carro_pelo_ID():
    database_inicialize()

    criar_carro_para_test()

    id_carro = 1
    response = client.delete(f"/carros/{id_carro}/")
    assert response.status_code == 204
