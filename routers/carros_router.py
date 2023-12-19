from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.carro_model import Carros
from shared.dependencies import get_db

# instanciando o api router
router = APIRouter(prefix='/carros')


class CarroResponse(BaseModel):
    id: int
    nome: str
    ano: int
    modelo: str


class CarroRequest(BaseModel):
    nome: str
    ano: int
    modelo: str


# metodo listar carros
@router.get('/', response_model=List[CarroResponse])
def listar_carros(db: Session = Depends(get_db)) -> List[CarroResponse]:
    return db.query(Carros).all()


# metodo criar carro
@router.post('/', response_model=CarroResponse, status_code=202)
def criar_carro(carro_request: CarroRequest, db: Session = Depends(get_db)) -> CarroResponse:
    # carro = Carros(nome= carro.nome, ano=carro.ano, modelo=carro.modelo)
    carro = Carros(
        nome=carro_request.nome,
        ano=carro_request.ano,
        modelo=carro_request.modelo
    )
    db.add(carro)
    db.commit()
    db.refresh(carro)

    return CarroResponse(
        id=carro.id,
        nome=carro.nome,
        ano=carro.ano,
        modelo=carro.modelo
    )
