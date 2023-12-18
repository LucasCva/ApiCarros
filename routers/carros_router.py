from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

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
def listar_carros():
    return [
        CarroResponse(id=1, nome='Camaro', ano=2022, modelo='Fiat')
    ]


# metodo criar carro
@router.post('/', response_model=List[CarroResponse], status_code=202)
def criar_carro(carro: CarroRequest):
    return [
        CarroResponse(id=1, nome=carro.nome, ano=carro.ano, modelo=carro.modelo)
    ]
